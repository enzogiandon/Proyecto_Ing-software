from datetime import date

from django import forms
from django.core.exceptions import ValidationError

from .models import Comercio, ImportacionRemitos, Marca, Remito


class RemitoForm(forms.ModelForm):
    def clean_total(self):
        total = self.cleaned_data.get("total")
        if total is not None and total <= 0:
            raise ValidationError("El monto total tiene que ser mayor a cero.")
        return total

    def clean_numero(self):
        numero = self.cleaned_data.get("numero")
        if self.instance and self.instance.pk and numero != self.instance.numero:
            raise ValidationError("No está permitido modificar el número de remito una vez creado.")
        return numero

    def clean(self):
        cleaned_data = super().clean()
        numero = cleaned_data.get("numero")
        marca = cleaned_data.get("marca")

        if numero and marca:
            qs = Remito.objects.filter(numero=numero, marca=marca)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                self.add_error(
                    "numero",
                    "El número de remito debe ser único por marca proveedora.",
                )

        return cleaned_data


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


class MultipleFileInput(forms.FileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault(
            "widget",
            MultipleFileInput(attrs={"class": "form-control", "accept": ".csv, .xlsx, .xls"}),
        )
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class ImportacionRemitosForm(forms.ModelForm):
    archivo = MultipleFileField(
        label="Archivos",
        help_text="Puede seleccionar uno o varios archivos.",
    )

    class Meta:
        model = ImportacionRemitos
        fields = ["archivo", "marca"]
        widgets = {
            "marca": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["marca"].required = False


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
