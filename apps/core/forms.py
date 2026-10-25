from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import transaction

from .models import Roles, Transportista, Usuario, Vehiculo


class LoginForm(AuthenticationForm):
    error_messages = {
        "invalid_login": "El usuario o la contraseña ingresados son incorrectos. Inténtalo de nuevo.",
        "inactive": "Esta cuenta se encuentra suspendida.",
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Usuario"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Contraseña"}
        )

    def get_user(self) -> Usuario:
        user = super().get_user()
        assert isinstance(user, Usuario)
        return user

class EmpleadoCreateForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="Contraseña",
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="Confirmar contraseña",
    )

    class Meta:
        model = Usuario
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "dni",
            "telefono",
            "rol",
        ]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre de usuario"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"}),
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Apellido"}),
            "dni": forms.TextInput(attrs={"class": "form-control", "placeholder": "DNI"}),
            "telefono": forms.TextInput(attrs={"class": "form-control", "placeholder": "Teléfono"}),
            "rol": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["rol"].choices = [
            (Roles.ADMINISTRATIVO, Roles.ADMINISTRATIVO.label),
            (Roles.TRANSPORTISTA, Roles.TRANSPORTISTA.label),
        ]

    def clean_dni(self):
        dni = self.cleaned_data["dni"]
        if Usuario.objects.filter(dni=dni).exists():
            raise ValidationError("El empleado ya se encuentra registrado.")
        return dni

    def clean_password(self):
        password = self.cleaned_data["password"]
        validate_password(password, user=self.instance)
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            self.add_error("password_confirm", "Las contraseñas no coinciden.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            with transaction.atomic():
                user.save()
                if user.rol == Roles.TRANSPORTISTA:
                    Transportista.objects.get_or_create(usuario=user)
        return user


class EmpleadoUpdateForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "dni",
            "telefono",
            "rol",
        ]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre de usuario"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"}),
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Apellido"}),
            "dni": forms.TextInput(attrs={"class": "form-control", "placeholder": "DNI"}),
            "telefono": forms.TextInput(attrs={"class": "form-control", "placeholder": "Teléfono"}),
            "rol": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["rol"].choices = [
            (Roles.ADMINISTRATIVO, Roles.ADMINISTRATIVO.label),
            (Roles.TRANSPORTISTA, Roles.TRANSPORTISTA.label),
        ]

    def clean_dni(self):
        dni = self.cleaned_data["dni"]
        if Usuario.objects.filter(dni=dni).exclude(pk=self.instance.pk).exists():
            raise ValidationError("El empleado ya se encuentra registrado.")
        return dni

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit and user.rol == Roles.TRANSPORTISTA:
            Transportista.objects.get_or_create(usuario=user)
        return user

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
