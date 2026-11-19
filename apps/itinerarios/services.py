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

    ocupados = {
        t.pk: t
        for t in Transportista.objects.filter(
            pk__in=[t.pk for t in transportistas],
            itinerarios__fecha=fecha,
        )
    }

    itinerarios = []
    for transportista in transportistas:
        if transportista.vehiculo_id is None:
            raise ValidationError(
                f"El transportista {transportista} no tiene un vehículo asignado."
            )
        if transportista.pk in ocupados:
            raise ValidationError(
                f"El transportista {transportista} ya tiene un itinerario "
                f"asignado para el {fecha:%d/%m/%Y}."
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
    itinerario: Itinerario, comercios: Iterable[Comercio]
) -> list[Parada]:
    itinerario = Itinerario.objects.select_for_update().get(pk=itinerario.pk)

    comercios_seleccionados = list(comercios)
    if not comercios_seleccionados:
        raise ValidationError("Seleccioná al menos un comercio.")

    comercios_seleccionados_ids = {c.id for c in comercios_seleccionados}

    # 1. Paradas existentes en este itinerario
    paradas_existentes = list(itinerario.paradas.select_related("comercio").order_by("orden", "id"))
    paradas_existentes_por_comercio = {p.comercio_id: p for p in paradas_existentes}

    # 2. Desasignar comercios desmarcados (solo paradas en estado PENDIENTE)
    for p in paradas_existentes:
        if p.comercio_id not in comercios_seleccionados_ids and p.estado == EstadoParada.PENDIENTE:
            Remito.objects.filter(parada=p).update(
                parada=None,
                estado=EstadoRemito.PENDIENTE,
            )
            p.delete()
            paradas_existentes_por_comercio.pop(p.comercio_id, None)

    # 3. Agregar comercios nuevos
    max_orden = (
        itinerario.paradas.aggregate(max_orden=models.Max("orden"))["max_orden"] or 0
    )

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

    # 4. Reenumerar orden de paradas restantes
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

