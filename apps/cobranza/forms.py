from decimal import Decimal

from django import forms
from django.forms import BaseInlineFormSet, formset_factory, inlineformset_factory

from .models import Cobranza, DetallePago, EstadoCobranza


class ValidarCobranzaForm(forms.ModelForm):
    class Meta:
        model = Cobranza
        fields = ["observacion_ajuste"]
        widgets = {
            "observacion_ajuste": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Detallar el motivo en caso de que difiera o haya pagos no encontrados...",
                }
            ),
        }


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Permitir que venga vacío (None) para detectar pagos "no encontrados"
        self.fields["monto_verificado"].required = False


class BaseDetallePagoFormSet(BaseInlineFormSet):
    """
    Calcula el estado resultante de la cobranza evaluando todos los detalles.
    """

    def clean(self):
        super().clean()
        if any(self.errors):
            return

        total_declarado = Decimal("0.00")
        total_verificado = Decimal("0.00")
        hay_pago_no_encontrado = False

        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            if not hasattr(form, "cleaned_data"):
                continue

            # Tomamos el monto declarado desde la instancia original
            monto_decl = form.instance.monto_declarado or Decimal("0.00")
            total_declarado += monto_decl

            monto_verif = form.cleaned_data.get("monto_verificado")

            # Regla de prioridad 1: Falta verificar algún pago
            if monto_verif is None:
                hay_pago_no_encontrado = True
            else:
                total_verificado += monto_verif

        # Determinación de estado según prioridades
        if hay_pago_no_encontrado:
            self.estado_calculado = EstadoCobranza.NO_ENCONTRADO
        elif total_declarado != total_verificado:
            self.estado_calculado = EstadoCobranza.DIFIERE
        else:
            self.estado_calculado = EstadoCobranza.APROBADO


DetallePagoFormSet = inlineformset_factory(
    parent_model=Cobranza,
    model=DetallePago,
    form=DetallePagoValidarForm,
    formset=BaseDetallePagoFormSet,
    extra=0,
    can_delete=False,
)


class AjusteItemForm(forms.Form):
    detalle_id = forms.IntegerField(widget=forms.HiddenInput())
    importe_nuevo = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal("0.00"),
        widget=forms.NumberInput(
            attrs={"class": "form-control form-control-sm text-end input-nuevo", "step": "0.01"}
        ),
    )
    motivo = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-sm input-motivo",
                "placeholder": "Motivo del ajuste para este medio de pago...",
            }
        ),
        required=True,
    )

    def clean_motivo(self):
        motivo = self.cleaned_data.get("motivo", "").strip()
        if not motivo:
            raise forms.ValidationError("Debe indicar obligatoriamente el motivo del ajuste.")
        return motivo


AjusteItemFormSet = formset_factory(AjusteItemForm, extra=0)
