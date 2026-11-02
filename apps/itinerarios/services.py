from collections.abc import Iterable
from datetime import date

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.core.models import Transportista
from apps.remitos.models import Comercio, EstadoRemito, Remito

from .models import EstadoItinerario, Itinerario, Parada, RutaGuardada


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
    itinerario: Itinerario, comercios: Iterable[Comercio]
) -> list[Parada]:
    itinerario = Itinerario.objects.select_for_update().get(pk=itinerario.pk)
    if itinerario.paradas.exists():
        raise ValidationError("El itinerario seleccionado ya tiene paradas asignadas.")

    comercios = list(comercios)
    if not comercios:
        raise ValidationError("Seleccioná al menos un comercio.")

    paradas = []
    for comercio in comercios:
        remitos_pendientes = Remito.objects.filter(
            comercio=comercio,
            estado=EstadoRemito.PENDIENTE,
            eliminado=False,
        )
        if not remitos_pendientes.exists():
            raise ValidationError(
                f'El comercio "{comercio}" ya no tiene remitos pendientes.'
            )

        parada = Parada.objects.create(
            itinerario=itinerario,
            comercio=comercio,
            orden=len(paradas) + 1,
        )
        remitos_pendientes.update(
            parada=parada,
            estado=EstadoRemito.ASIGNADO,
        )
        paradas.append(parada)

    return paradas


def ordenar_itinerario_segun_ruta(
    itinerario: Itinerario, ruta_guardada: RutaGuardada
) -> list[Parada]:
    """Ordena las paradas del itinerario:
    primero los comercios que figuran en la ruta (por prioridad), y los que no están en la ruta se colocan al final.
    """
    paradas = list(itinerario.paradas.all())

    prioridades = dict(ruta_guardada.detalles.values_list("comercio_id", "prioridad"))

    paradas_con_ruta = []
    paradas_sin_ruta = []

    for parada in paradas:
        if parada.comercio_id in prioridades:
            paradas_con_ruta.append(parada)
        else:
            paradas_sin_ruta.append(parada)

    paradas_con_ruta.sort(key=lambda p: prioridades[p.comercio_id])

    paradas_finales = paradas_con_ruta + paradas_sin_ruta

    with transaction.atomic():
        for orden_visita, parada in enumerate(paradas_finales, start=1):
            parada.orden = orden_visita

        Parada.objects.bulk_update(paradas_finales, fields=["orden"])

    return paradas_finales
