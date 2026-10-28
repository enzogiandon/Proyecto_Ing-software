from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import transaction
from django.contrib.auth import get_user_model

from .models import Grupos, Transportista, Usuario, Vehiculo

Usuario = get_user_model()


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


class GrupoMultipleChoiceField(forms.ModelMultipleChoiceField):
    """Muestra los nombres legibles de cada grupo en los checkboxes."""

    def label_from_instance(self, obj):
        try:
            return Grupos(obj.name).label
        except ValueError:
            return obj.name


class EmpleadoCreateForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="Contraseña",
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="Confirmar contraseña",
    )
    grupos = GrupoMultipleChoiceField(
        queryset=Group.objects.filter(name__in=Grupos.values).order_by("name"),
        required=True,
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
        label="Grupos / Roles asignados",
    )

    class Meta:
        model = Usuario
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "telefono",
            "grupos",
        ]
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nombre de usuario"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email"}
            ),
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nombre"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Apellido"}
            ),
            "telefono": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Teléfono"}
            ),
        }

    def clean_username(self):
        username = self.cleaned_data["username"]
        if Usuario.objects.filter(username=username).exists():
            raise ValidationError("El empleado ya se encuentra registrado.")
        return username

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
                nuevos_grupos = self.cleaned_data.get("grupos", [])
                user.groups.set(nuevos_grupos)

                nombres_grupos = [g.name for g in nuevos_grupos]
                if Grupos.TRANSPORTISTA in nombres_grupos:
                    Transportista.objects.get_or_create(usuario=user)
        return user


class EmpleadoUpdateForm(forms.ModelForm):
    grupos = GrupoMultipleChoiceField(
        queryset=Group.objects.filter(name__in=Grupos.values).order_by("name"),
        required=True,
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
        label="Grupos / Roles asignados",
    )

    class Meta:
        model = Usuario
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "telefono",
            "grupos",
        ]
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nombre de usuario"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email"}
            ),
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nombre"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Apellido"}
            ),
            "telefono": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Teléfono"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["grupos"].initial = self.instance.groups.filter(
                name__in=Grupos.values
            )

    def clean_username(self):
        username = self.cleaned_data["username"]
        if (
            Usuario.objects.filter(username=username)
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise ValidationError("El empleado ya se encuentra registrado.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            with transaction.atomic():
                user.save()
                nuevos_grupos = self.cleaned_data.get("grupos", [])
                user.groups.set(nuevos_grupos)

                nombres_grupos = [g.name for g in nuevos_grupos]
                if Grupos.TRANSPORTISTA in nombres_grupos:
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
