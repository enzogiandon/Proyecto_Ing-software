from decimal import Decimal

from django import forms
from django.forms import BaseInlineFormSet, formset_factory, inlineformset_factory

from .models import AjusteCobranza, Cobranza, DetallePago, EstadoCobranza


class ValidarCobranzaForm(forms.ModelForm):
    class Meta:
        model = Cobranza
        fields = ["observacion"]
        widgets = {
            "observacion": forms.Textarea(
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
        # Permitir que el campo venga vacío en el POST para transformarlo en 0
        self.fields["monto_verificado"].required = False

    def has_changed(self):
        # Si la instancia no tenía monto_verificado (None) o se limpió a 0.00, forzamos que guarde
        if self.instance and self.instance.pk and self.instance.monto_verificado is None:
            return True
        return super().has_changed()

    def clean_monto_verificado(self):
        monto = self.cleaned_data.get("monto_verificado")
        if monto is None or monto == "":
            return Decimal("0.00")
        return monto


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

        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            if not hasattr(form, "cleaned_data"):
                continue

            # Tomamos el monto declarado desde la instancia original
            monto_decl = form.instance.monto_declarado or Decimal("0.00")
            total_declarado += monto_decl

            monto_verif = form.cleaned_data.get("monto_verificado") or Decimal("0.00")
            total_verificado += monto_verif

        # Determinación de estado según prioridades
        if total_declarado != total_verificado:
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


class AjusteCobranzaForm(forms.ModelForm):
    class Meta:
        model = AjusteCobranza
        fields = ["medio", "monto", "motivo"]
        widgets = {
            "medio": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "monto": forms.NumberInput(
                attrs={
                    "class": "form-control text-end",
                    "step": "0.01",
                    "placeholder": "0.00 (puede ser positivo o negativo)",
                }
            ),
            "motivo": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Justificación del ajuste o corrección...",
                }
            ),
        }

    def clean_monto(self):
        monto = self.cleaned_data.get("monto")
        if monto is None or monto == Decimal("0.00"):
            raise forms.ValidationError("El monto del ajuste no puede ser 0.")
        return monto

    def clean_motivo(self):
        motivo = self.cleaned_data.get("motivo", "").strip()
        if not motivo:
            raise forms.ValidationError("Debe indicar obligatoriamente el motivo del ajuste.")
        return motivo
