from django import forms
from django.db.models import Q

from apps.core.models import Grupos, Transportista
from apps.remitos.models import Comercio, EstadoRemito, Remito

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
    remitos = forms.ModelMultipleChoiceField(
        label="Remitos",
        queryset=Remito.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    comercios = forms.ModelMultipleChoiceField(
        queryset=Comercio.objects.none(),
        required=False,
        widget=forms.MultipleHiddenInput,
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

        # Filtro de remitos elegibles:
        # 1. Remitos pendientes sin parada asignada
        # 2. Remitos de paradas PENDIENTES ya pertenecientes a este itinerario
        filtro_remitos = Q(
            estado=EstadoRemito.PENDIENTE,
            parada__isnull=True,
        )
        if itinerario_obj:
            filtro_remitos |= Q(
                parada__itinerario=itinerario_obj,
                parada__estado=EstadoParada.PENDIENTE,
            )

        remitos_qs = (
            Remito.objects.filter(filtro_remitos)
            .select_related("comercio", "marca")
            .order_by("comercio__razon_social", "numero")
        )
        self.fields["remitos"].queryset = remitos_qs

        # Si itinerario_obj está presente y no es bound, inicializar initial
        if itinerario_obj and not self.is_bound:
            self.initial["itinerario"] = itinerario_obj.pk
            remitos_actuales = list(
                Remito.objects.filter(
                    parada__itinerario=itinerario_obj,
                    parada__estado=EstadoParada.PENDIENTE,
                ).values_list("id", flat=True)
            )
            self.initial["remitos"] = remitos_actuales

        # Estructura comercios_agrupados para renderizar el acordeón
        self.comercios_agrupados = self._build_comercios_agrupados(remitos_qs)

        # Poblar comercios.queryset para compatibilidad
        comercios_ids = {g["comercio"].id for g in self.comercios_agrupados}
        self.fields["comercios"].queryset = Comercio.objects.filter(id__in=comercios_ids).order_by("razon_social")

    def _build_comercios_agrupados(self, remitos_qs):
        if self.is_bound:
            if hasattr(self.data, "getlist"):
                raw_selected = self.data.getlist("remitos")
            else:
                val = self.data.get("remitos", [])
                raw_selected = val if isinstance(val, (list, tuple, set)) else [val]
        else:
            raw_selected = self.initial.get("remitos", [])

        selected_ids = {str(item) for item in raw_selected if item}

        agrupados_dict = {}
        for remito in remitos_qs:
            comercio = remito.comercio
            if comercio.id not in agrupados_dict:
                agrupados_dict[comercio.id] = {
                    "comercio": comercio,
                    "remitos": [],
                    "total_count": 0,
                    "selected_count": 0,
                    "total_monto": 0,
                    "selected_monto": 0,
                }
            grupo = agrupados_dict[comercio.id]
            is_selected = str(remito.id) in selected_ids
            grupo["remitos"].append({
                "remito": remito,
                "is_selected": is_selected,
            })
            grupo["total_count"] += 1
            grupo["total_monto"] += remito.total
            if is_selected:
                grupo["selected_count"] += 1
                grupo["selected_monto"] += remito.total

        comercios_lista = list(agrupados_dict.values())
        for grupo in comercios_lista:
            tot = grupo["total_count"]
            sel = grupo["selected_count"]
            grupo["all_selected"] = (sel == tot and tot > 0)
            grupo["is_indeterminate"] = (0 < sel < tot)

        return comercios_lista

    def clean(self):
        cleaned_data = super().clean()
        remitos = cleaned_data.get("remitos")
        comercios = cleaned_data.get("comercios")

        if not remitos and not comercios:
            raise forms.ValidationError("Seleccioná al menos un remito para asignar.")

        if not remitos and comercios:
            cleaned_data["remitos"] = Remito.objects.filter(
                comercio__in=comercios,
                estado=EstadoRemito.PENDIENTE,
                parada__isnull=True,
            )

        return cleaned_data
