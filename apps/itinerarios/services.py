from collections.abc import Iterable
from datetime import date

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.core.models import Transportista
from apps.remitos.models import Comercio, EstadoRemito, Remito

from .models import EstadoItinerario, Itinerario, Parada


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
                estado=EstadoItinerario.PENDIENTE,
            )
        )
    return Itinerario.objects.bulk_create(itinerarios)


@transaction.atomic
def crear_paradas(
    itinerario: Itinerario, comercios: Iterable[Comercio]
) -> list[Parada]:
    itinerario = Itinerario.objects.select_for_update().get(pk=itinerario.pk)
    if itinerario.paradas.exists():
        raise ValidationError(
            "El itinerario seleccionado ya tiene paradas asignadas."
        )

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