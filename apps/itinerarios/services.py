from collections.abc import Iterable
from datetime import date

from django.core.exceptions import ValidationError
from django.db import models, transaction

from apps.core.models import Transportista
from apps.remitos.models import Comercio, EstadoRemito, Remito

from .models import EstadoItinerario, EstadoParada, Itinerario, Parada, RutaGuardada


@transaction.atomic
def crear_itinerarios(
    transportistas: Iterable[Transportista], fecha: date
) -> list[Itinerario]:
    transportistas = list(transportistas)
    if not transportistas:
        raise ValidationError("Seleccioná al menos un transportista.")

    itinerarios = []
    for transportista in transportistas:
        if transportista.vehiculo_id is None:
            raise ValidationError(
                f"El transportista {transportista} no tiene un vehículo asignado."
            )
        itinerarios.append(
            Itinerario(
                fecha=fecha,
                transportista=transportista,
                vehiculo=transportista.vehiculo,
                estado=EstadoItinerario.ASIGNADO,
            )
        )
    return Itinerario.objects.bulk_create(itinerarios)


@transaction.atomic
def crear_paradas(
    itinerario: Itinerario,
    comercios: Iterable[Comercio] = None,
    remitos: Iterable[Remito] = None,
) -> list[Parada]:
    itinerario = Itinerario.objects.select_for_update().get(pk=itinerario.pk)

    if itinerario.estado in [EstadoItinerario.EN_CURSO, EstadoItinerario.FINALIZADO]:
        raise ValidationError(
            f"No se pueden agregar ni modificar paradas a un itinerario en estado '{itinerario.get_estado_display()}'."
        )

    # 1. Normalizar selección
    if remitos is not None:
        remitos_seleccionados = list(remitos)
        if not remitos_seleccionados:
            raise ValidationError("Seleccioná al menos un remito.")
        remitos_por_comercio = {}
        for r in remitos_seleccionados:
            remitos_por_comercio.setdefault(r.comercio_id, []).append(r)
        comercios_ids = set(remitos_por_comercio.keys())
        comercios_seleccionados = None
    elif comercios is not None:
        comercios_seleccionados = list(comercios)
        if not comercios_seleccionados:
            raise ValidationError("Seleccioná al menos un comercio.")
        comercios_ids = {c.id for c in comercios_seleccionados}
        remitos_por_comercio = None
    else:
        raise ValidationError("Debes especificar comercios o remitos para asignar.")

    # 2. Paradas existentes en este itinerario
    paradas_existentes = list(itinerario.paradas.select_related("comercio").order_by("orden", "id"))
    paradas_existentes_por_comercio = {p.comercio_id: p for p in paradas_existentes}

    # 3. Desasignar o desvincular paradas/remitos desmarcados (solo paradas PENDIENTE)
    for p in paradas_existentes:
        if p.estado != EstadoParada.PENDIENTE:
            continue

        if p.comercio_id not in comercios_ids:
            Remito.objects.filter(parada=p).update(
                parada=None,
                estado=EstadoRemito.PENDIENTE,
            )
            p.delete()
            paradas_existentes_por_comercio.pop(p.comercio_id, None)
        elif remitos_por_comercio is not None:
            remitos_comercio_ids = {r.id for r in remitos_por_comercio[p.comercio_id]}
            Remito.objects.filter(parada=p).exclude(id__in=remitos_comercio_ids).update(
                parada=None,
                estado=EstadoRemito.PENDIENTE,
            )
            Remito.objects.filter(id__in=remitos_comercio_ids).update(
                parada=p,
                estado=EstadoRemito.ASIGNADO,
            )

    # 4. Agregar comercios nuevos
    max_orden = (
        itinerario.paradas.aggregate(max_orden=models.Max("orden"))["max_orden"] or 0
    )

    if remitos_por_comercio is not None:
        for comercio_id, remitos_lista in remitos_por_comercio.items():
            if comercio_id not in paradas_existentes_por_comercio:
                comercio = Comercio.objects.get(pk=comercio_id)
                max_orden += 1
                nueva_parada = Parada.objects.create(
                    itinerario=itinerario,
                    comercio=comercio,
                    orden=max_orden,
                    estado=EstadoParada.PENDIENTE,
                )
                Remito.objects.filter(id__in=[r.id for r in remitos_lista]).update(
                    parada=nueva_parada,
                    estado=EstadoRemito.ASIGNADO,
                )
                paradas_existentes_por_comercio[comercio_id] = nueva_parada
    else:
        for comercio in comercios_seleccionados:
            if comercio.id not in paradas_existentes_por_comercio:
                remitos_pendientes = Remito.objects.filter(
                    comercio=comercio,
                    estado=EstadoRemito.PENDIENTE,
                )
                if not remitos_pendientes.exists():
                    raise ValidationError(
                        f'El comercio "{comercio}" ya no tiene remitos pendientes.'
                    )

                max_orden += 1
                nueva_parada = Parada.objects.create(
                    itinerario=itinerario,
                    comercio=comercio,
                    orden=max_orden,
                    estado=EstadoParada.PENDIENTE,
                )
                remitos_pendientes.update(
                    parada=nueva_parada,
                    estado=EstadoRemito.ASIGNADO,
                )
                paradas_existentes_por_comercio[comercio.id] = nueva_parada

    # 5. Reenumerar orden de paradas restantes
    paradas_finales = list(itinerario.paradas.all().order_by("orden", "id"))
    for idx, p in enumerate(paradas_finales, start=1):
        if p.orden != idx:
            p.orden = idx
            p.save(update_fields=["orden"])

    return paradas_finales


def ordenar_itinerario_segun_ruta(
    itinerario: Itinerario, ruta_guardada: RutaGuardada
) -> list[Parada]:
    """Ordena las paradas del itinerario preservando los slots de paradas no reordenables:
    - Las paradas finalizadas o resueltas conservan intacta su posición ordinal histórica (slot).
    - Las paradas pendientes se distribuyen ordenadas según la ruta guardada en los slots disponibles.
    - Las paradas sin ruta se colocan al final de los slots pendientes.
    """
    paradas = list(itinerario.paradas.all().order_by("orden", "id"))
    prioridades = dict(ruta_guardada.detalles.values_list("comercio_id", "prioridad"))

    # Identificar paradas fijas (finalizadas o resueltas) vs reordenables (pendientes)
    paradas_pendientes = []
    slots_disponibles = []

    for parada in paradas:
        if parada.estado in (EstadoParada.FINALIZADA, EstadoParada.RESUELTO):
            # Conserva intacta su posición ordinal histórica en el itinerario
            continue
        paradas_pendientes.append(parada)
        slots_disponibles.append(parada.orden)

    # Ordenar las paradas pendientes: primero las que están en la ruta por prioridad, luego las que no
    paradas_con_ruta = []
    paradas_sin_ruta = []

    for parada in paradas_pendientes:
        if parada.comercio_id in prioridades:
            paradas_con_ruta.append(parada)
        else:
            paradas_sin_ruta.append(parada)

    paradas_con_ruta.sort(key=lambda p: prioridades[p.comercio_id])
    pendientes_ordenadas = paradas_con_ruta + paradas_sin_ruta

    # Asignar a cada parada pendiente ordenada su slot correspondiente
    paradas_a_actualizar = []
    for slot, parada in zip(slots_disponibles, pendientes_ordenadas):
        if parada.orden != slot:
            parada.orden = slot
            paradas_a_actualizar.append(parada)

    if paradas_a_actualizar:
        with transaction.atomic():
            Parada.objects.bulk_update(paradas_a_actualizar, fields=["orden"])

    return list(itinerario.paradas.all().order_by("orden", "id"))

