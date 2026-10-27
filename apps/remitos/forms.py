from datetime import date

from django import forms
from django.core.exceptions import ValidationError

from .models import Comercio, ImportacionRemitos, Marca, Remito


class RemitoForm(forms.ModelForm):
    def clean_fecha_pactada(self):
        fecha = self.cleaned_data.get("fecha_pactada")
        if not self.instance.pk and fecha and fecha < date.today():
            raise ValidationError("La fecha pactada no puede ser anterior a hoy.")
        return fecha

    def clean_total(self):
        total = self.cleaned_data.get("total")
        if total is not None and total <= 0:
            raise ValidationError("El monto total tiene que ser mayor a cero.")
        return total


    class Meta:
        model = Remito
        fields = [
            "numero",
            "marca",
            "comercio",
            "total",
        ]
        widgets = {
            "numero": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nº de remito"}
            ),
            "marca": forms.Select(attrs={"class": "form-select"}),
            "comercio": forms.Select(attrs={"class": "form-select"}),
            "total": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Total a cobrar por el transportista",
                    "step": "0.01",
                    "min": "0.01",
                }
            ),
        }


<<<<<<< HEAD
class ItemRemitoForm(forms.ModelForm):
    producto_nombre = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control item-producto-input",
            "placeholder": "Escribí o seleccioná un producto...",
            "autocomplete": "off",
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["producto"].required = False
        if self.instance and self.instance.pk and getattr(self.instance, "producto", None):
            self.fields["producto_nombre"].initial = self.instance.producto.nombre

    def clean_precio_unitario(self):
        precio = self.cleaned_data.get("precio_unitario")
        if precio is not None and precio <= Decimal(0):
            raise ValidationError("El precio unitario debe ser mayor a 0")
        return precio

    def clean(self):
        cleaned_data = super().clean()
        prod = cleaned_data.get("producto")
        prod_nombre = (self.cleaned_data.get("producto_nombre") or self.data.get(self.add_prefix("producto_nombre")) or "").strip()

        if not prod and prod_nombre:
            prod = Producto.objects.filter(nombre__iexact=prod_nombre).first()
            if not prod:
                prod = Producto.objects.create(nombre=prod_nombre, activo=True)
            cleaned_data["producto"] = prod
            self.instance.producto = prod
            if "producto" in self._errors:
                del self._errors["producto"]

        if not prod and not prod_nombre and not self.cleaned_data.get("DELETE", False):
            self.add_error("producto", "Debes ingresar o seleccionar un producto.")

        return cleaned_data

    class Meta:
        model = ItemRemito
        fields = ["producto", "cantidad", "precio_unitario"]
        widgets = {
            "producto": forms.Select(attrs={"class": "form-select item-producto-select"}),
            "cantidad": forms.NumberInput(attrs={"min": "1", "class": "form-control item-cantidad-input"}),
            "precio_unitario": forms.NumberInput(attrs={"step": "0.01", "min": "0.00", "class": "form-control item-precio-input"}),
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


=======
>>>>>>> d48cdfd927014556ad1cd7541bed245e52f9e676
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
