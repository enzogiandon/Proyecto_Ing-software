from datetime import date
from decimal import Decimal

from django import forms
from django.core.exceptions import ValidationError

from .models import Comercio, ImportacionRemitos, ItemRemito, Marca, Producto, Remito


class RemitoForm(forms.ModelForm):
    def clean_fecha_pactada(self):
        fecha = self.cleaned_data.get("fecha_pactada")
        if not self.instance.pk and fecha and fecha < date.today():
            raise ValidationError("La fecha pactada no puede ser anterior a hoy.")
        return fecha

    class Meta:
        model = Remito
        fields = [
            "numero",
            "marca",
            "fecha_emision",
            "fecha_pactada",
            "comercio",
        ]
        widgets = {
            "numero": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nº de remito"}
            ),
            "marca": forms.Select(attrs={"class": "form-select"}),
            "fecha_emision": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "fecha_pactada": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "comercio": forms.Select(attrs={"class": "form-select"}),
        }


class ItemRemitoForm(forms.ModelForm):
    def clean_precio_unitario(self):
        precio = self.cleaned_data.get("precio_unitario")
        if precio is not None and precio <= Decimal(0):
            raise ValidationError("El precio unitario debe ser mayor a 0")
        return precio

    class Meta:
        model = ItemRemito
        fields = ["producto", "cantidad", "precio_unitario"]
        widgets = {
            "cantidad": forms.NumberInput(attrs={"min": "1"}),
            "precio_unitario": forms.NumberInput(attrs={"step": "0.01", "min": "0.00"}),
        }


class BaseItemRemitoFormSet(forms.BaseInlineFormSet):
    """Valida que no haya productos duplicados entre las filas del remito."""

    def clean(self):
        super().clean()
        if any(self.errors):
            return

        productos_vistos = set()
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            if not form.cleaned_data or not form.cleaned_data.get("producto"):
                continue

            producto = form.cleaned_data.get("producto")

            if producto in productos_vistos:
                raise ValidationError(
                    f'El producto "{producto.nombre}" está repetido en más de una fila.'
                    " Modificá la cantidad en lugar de agregarlo nuevamente."
                )
            productos_vistos.add(producto)


ItemRemitoFormSet = forms.inlineformset_factory(
    parent_model=Remito,
    model=ItemRemito,
    form=ItemRemitoForm,
    formset=BaseItemRemitoFormSet,
    fields=["producto", "cantidad", "precio_unitario"],
    extra=1,
    can_delete=True,
)


class ImportacionRemitosForm(forms.ModelForm):
    class Meta:
        model = ImportacionRemitos
        fields = ["archivo", "marca"]
        widgets = {
            "marca": forms.Select(attrs={"class": "form-select"}),
            "archivo": forms.FileInput(
                attrs={"class": "form-control", "accept": ".csv, xlsx, xls"}
            ),
        }


class ProductoForm(forms.ModelForm):
    activo = forms.BooleanField(
        label="Estado",
        initial=True,
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    class Meta:
        model = Producto
        fields = ["nombre", "marca", "codigo", "activo"]
        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Detergente Vajilla Citrus 750ml (Caja x12)",
                }
            ),
            "marca": forms.Select(
                attrs={"class": "form-select", "placeholder": "Marca"}
            ),
            "codigo": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "1234 1234"}
            ),
        }


class ComercioForm(forms.ModelForm):
    class Meta:
        model = Comercio
        fields = ["razon_social", "cuit", "domicilio", "telefono"]
        widgets = {
            "razon_social": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Coca-Cola"}
            ),
            "cuit": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "20123456783"}
            ),
            "domicilio": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Calle falsa 123"}
            ),
            "telefono": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "11 1234 1234"}
            ),
        }


class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ["nombre", "cuit", "telefono", "email"]
        widgets = {
            "nombre": forms.TextInput(
                attrs={"class": "form-select", "placeholder": "Razon social"}
            ),
            "cuit": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "CUIT"}
            ),
            "telefono": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "11 1234 1234"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "email@mail.com"}
            ),
        }
