from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group, Permission

from .models import Transportista, Usuario, Roles


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

class UserRegisterForm(forms.ModelForm):
    permisos = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
        label="Permisos del sistema"
    )
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}), label="Contraseña")
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}), label="Confirmar contraseña")

    class Meta:
        model = Usuario
        fields = ["username", "email", "first_name", "last_name", "dni", "telefono", "rol", "permisos", "groups", "is_active"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre de usuario"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"}),
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Apellido"}),
            "dni": forms.TextInput(attrs={"class": "form-control", "placeholder": "DNI"}),
            "telefono": forms.TextInput(attrs={"class": "form-control", "placeholder": "Teléfono"}),
            "rol": forms.Select(attrs={"class": "form-select"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"})
        }

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not password:
            return password

        if not any(char.isdigit() for char in password):
            raise forms.ValidationError("La contraseña debe contener al menos un digito")

        if len(password) < 8:
            raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres")

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data is None:
            cleaned_data = {}

        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Las contraseñas no coinciden")

        return cleaned_data


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"]) # Hashea la contraseña por seguridad
        if commit:
            user.save()
            user.save_m2m()

            if user.rol == Roles.TRANSPORTISTA:
                Transportista.objects.get_or_create(usuario=user)
        return user

