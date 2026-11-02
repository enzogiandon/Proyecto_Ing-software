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
