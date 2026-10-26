from django import forms

from apps.core.models import Roles, Transportista
from apps.remitos.models import Comercio, EstadoRemito

from .models import EstadoItinerario, Itinerario


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
                usuario__rol=Roles.TRANSPORTISTA,
                vehiculo__isnull=False,
            )
            .select_related("usuario", "vehiculo")
            .order_by("usuario__last_name", "usuario__first_name", "usuario__id")
        )


class CrearParadasForm(forms.Form):
    itinerario = forms.ModelChoiceField(
        label="Itinerario",
        queryset=Itinerario.objects.none(),
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    comercios = forms.ModelMultipleChoiceField(
        label="Comercios con remitos pendientes",
        queryset=Comercio.objects.none(),
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["itinerario"].queryset = (
            Itinerario.objects.filter(
                estado=EstadoItinerario.ASIGNADO,
                paradas__isnull=True,
            )
            .select_related("transportista__usuario", "vehiculo")
            .order_by("-fecha", "id")
        )
        self.fields["comercios"].queryset = (
            Comercio.objects.filter(
                remitos__estado=EstadoRemito.PENDIENTE,
                remitos__eliminado=False,
            )
            .distinct()
            .order_by("razon_social", "id")
        )
