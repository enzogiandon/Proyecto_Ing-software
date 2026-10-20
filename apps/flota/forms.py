from django import forms
from django.core.exceptions import ValidationError

from .models import Vehiculo


class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ["patente", "modelo", "poliza", "estado"]
        widgets = {
            "patente": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Patente"}
            ),
            "modelo": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Marca y modelo"}
            ),
            "poliza": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Número de póliza"}
            ),
            "estado": forms.Select(attrs={"class": "form-select"}),
        }

    def clean_patente(self):
        patente = self.cleaned_data["patente"].strip().upper()
        vehiculos = Vehiculo.objects.filter(patente__iexact=patente)
        if self.instance.pk:
            vehiculos = vehiculos.exclude(pk=self.instance.pk)
        if vehiculos.exists():
            raise ValidationError("Vehículo repetido")
        return patente
