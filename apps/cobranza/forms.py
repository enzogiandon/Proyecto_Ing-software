from django import forms
from django.forms import inlineformset_factory

from .models import Cobranza, DetallePago, EstadoCobranza


class ValidarCobranzaForm(forms.ModelForm):
    class Meta:
        model = Cobranza
        fields = ["estado", "observacion_ajuste"]
        widgets = {
            "estado": forms.Select(attrs={"class": "form-select"}),
            "observacion_ajuste": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Detallar el motivo en caso de diferir, rechazar o ajustar importes...",
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        estado = cleaned_data.get("estado")
        observacion = cleaned_data.get("observacion_ajuste")

        # Exigir observación si no se aprueba la cobranza
        if estado in [EstadoCobranza.DIFIERE, EstadoCobranza.NO_ENCONTRADO] and not observacion:
            self.add_error(
                "observacion_ajuste",
                "Es obligatorio documentar una observación cuando el estado es 'Difiere' o 'No encontrado'.",
            )
        return cleaned_data


class DetallePagoValidarForm(forms.ModelForm):
    class Meta:
        model = DetallePago
        fields = ["monto_verificado"]
        widgets = {
            "monto_verificado": forms.NumberInput(
                attrs={
                    "class": "form-control form-control-sm text-end input-monto-verificado",
                    "step": "0.01",
                    "min": "0.00",
                    "placeholder": "0.00",
                }
            ),
        }


DetallePagoFormSet = inlineformset_factory(
    parent_model=Cobranza,
    model=DetallePago,
    form=DetallePagoValidarForm,
    extra=0,
    can_delete=False,
)
