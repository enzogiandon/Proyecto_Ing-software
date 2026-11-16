from django import forms
from django.db.models import Q

from apps.core.models import Grupos, Transportista
from apps.remitos.models import Comercio, EstadoRemito

from .models import EstadoItinerario, EstadoParada, Itinerario


class TransportistaMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj: Transportista) -> str:
        nombre = obj.usuario.get_full_name() or obj.usuario.username
        return f"{nombre} - {obj.vehiculo.patente}"


class CrearItinerariosForm(forms.Form):
    fecha = forms.DateField(
        label="Fecha de entrega",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )
    transportistas = TransportistaMultipleChoiceField(
        label="Transportistas",
        queryset=Transportista.objects.none(),
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["transportistas"].queryset = (
            Transportista.objects.filter(
                usuario__is_active=True,
                usuario__groups__name=Grupos.TRANSPORTISTA,
                vehiculo__isnull=False,
            )
            .select_related("usuario", "vehiculo")
            .order_by("usuario__last_name", "usuario__first_name", "usuario__id")
        )


class CrearParadasForm(forms.Form):
    itinerario = forms.ModelChoiceField(
        label="Itinerario",
        queryset=Itinerario.objects.none(),
        widget=forms.Select(attrs={"class": "form-select", "id": "id_itinerario"}),
    )
    comercios = forms.ModelMultipleChoiceField(
        label="Comercios con remitos pendientes",
        queryset=Comercio.objects.none(),
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, itinerario_id=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["itinerario"].queryset = (
            Itinerario.objects.filter(
                estado=EstadoItinerario.ASIGNADO,
            )
            .select_related("transportista__usuario", "vehiculo")
            .order_by("-fecha", "id")
        )

        # Detectar el itinerario seleccionado
        itin_id = itinerario_id
        if not itin_id and self.is_bound:
            itin_id = self.data.get("itinerario")
        if not itin_id and "itinerario" in self.initial:
            itin_id = self.initial["itinerario"]

        itinerario_obj = None
        if itin_id:
            try:
                itinerario_obj = Itinerario.objects.filter(pk=itin_id).first()
            except (ValueError, TypeError):
                pass

        # Filtro de comercios:
        # Comercios con remitos PENDIENTES o comercios que ya tienen parada PENDIENTE en este itinerario
        filtro_comercios = Q(
            remitos__estado=EstadoRemito.PENDIENTE,
            remitos__eliminado=False,
        )
        if itinerario_obj:
            filtro_comercios |= Q(
                paradas__itinerario=itinerario_obj,
                paradas__estado=EstadoParada.PENDIENTE,
            )

        self.fields["comercios"].queryset = (
            Comercio.objects.filter(filtro_comercios)
            .distinct()
            .order_by("razon_social", "id")
        )

        # Pre-marcar los comercios que ya están en el itinerario si no viene de un POST
        if itinerario_obj and not self.is_bound:
            self.initial["itinerario"] = itinerario_obj.pk
            comercios_actuales = list(
                itinerario_obj.paradas.filter(estado=EstadoParada.PENDIENTE).values_list(
                    "comercio_id", flat=True
                )
            )
            self.initial["comercios"] = comercios_actuales
