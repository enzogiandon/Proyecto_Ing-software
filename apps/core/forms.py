from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Q

from .models import EstadoVehiculo, Grupos, Transportista, Usuario, Vehiculo


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
    vehiculo = forms.ModelChoiceField(
        queryset=Vehiculo.objects.none(),
        required=False,
        empty_label="Seleccione un vehículo (opcional)",
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Vehículo asignado",
    )

    class Meta:
        model = Usuario
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "telefono",
            "vehiculo",
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
        self.fields["vehiculo"].queryset = Vehiculo.objects.filter(
            transportista__isnull=True, estado="disponible"
        ).order_by("modelo", "patente")

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
                vehiculo = self.cleaned_data.get("vehiculo")
                
                if Grupos.TRANSPORTISTA in nombres_grupos:
                    perfil, _ = Transportista.objects.get_or_create(usuario=user)
                    perfil.vehiculo = vehiculo
                    perfil.save(update_fields=["vehiculo"])
                    
                    if vehiculo:
                        vehiculo.estado = EstadoVehiculo.ASIGNADO
                        vehiculo.save(update_fields=["estado"])

        return user

class EmpleadoUpdateForm(forms.ModelForm):
    # Campos de contraseña opcionales para edición
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Dejar en blanco para no modificar"}
        ),
        label="Nueva contraseña",
        required=False,
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirmar nueva contraseña"}
        ),
        label="Confirmar nueva contraseña",
        required=False,
    )

    grupos = GrupoMultipleChoiceField(
        queryset=Group.objects.filter(name__in=Grupos.values).order_by("name"),
        required=True,
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
        label="Grupos / Roles asignados",
    )
    vehiculo = forms.ModelChoiceField(
        queryset=Vehiculo.objects.none(),
        required=False,
        empty_label="Seleccione un vehículo (opcional)",
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Vehículo asignado",
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
            self.fields["username"].disabled = True
            self.fields["first_name"].disabled = True
            self.fields["last_name"].disabled = True

            perfil = getattr(self.instance, "perfil_transportista", None)
            
            # Vehículos disponibles + el vehículo actualmente asignado a este transportista
            qs_disponibles = Q(transportista__isnull=True, estado="disponible")
            if perfil and perfil.vehiculo_id:
                qs_final = Vehiculo.objects.filter(qs_disponibles | Q(pk=perfil.vehiculo_id))
                self.fields["vehiculo"].initial = perfil.vehiculo
            else:
                qs_final = Vehiculo.objects.filter(qs_disponibles)

            self.fields["vehiculo"].queryset = qs_final.order_by("modelo", "patente")

    def clean_grupos(self):
        grupos = self.cleaned_data.get("grupos")
        if not grupos:
            return grupos

        nombres_grupos = [getattr(g, "name", str(g)) for g in grupos]
        if Grupos.TRANSPORTISTA in nombres_grupos and len(nombres_grupos) > 1:
            raise ValidationError(
                "Un transportista no puede tener otros roles asignados."
            )
        return grupos

    def clean_username(self):
        username = self.cleaned_data["username"]
        if (
            Usuario.objects.filter(username=username)
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise ValidationError("El empleado ya se encuentra registrado.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        # Solo validamos si el usuario ingresó algo en alguno de los dos campos
        if password or password_confirm:
            if not password:
                self.add_error("password", "Debe ingresar una contraseña.")
            elif not password_confirm:
                self.add_error("password_confirm", "Debe confirmar la contraseña.")
            elif password != password_confirm:
                self.add_error("password_confirm", "Las contraseñas no coinciden.")
            else:
                # Si quitaste AUTH_PASSWORD_VALIDATORS = [] no dará errores de complejidad
                validate_password(password, user=self.instance)

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")

        # Actualiza el hash solo si se ingresó una nueva clave
        if password:
            user.set_password(password)

        if commit:
            with transaction.atomic():
                user.save()
                grupos = self.cleaned_data.get("grupos")
                if grupos is not None:
                    user.groups.set(grupos)

                nombres_grupos = [getattr(g, "name", str(g)) for g in user.groups.all()]
                es_transportista = Grupos.TRANSPORTISTA in nombres_grupos
                nuevo_vehiculo = self.cleaned_data.get("vehiculo")

                perfil = Transportista.objects.filter(usuario=user).first()

                if es_transportista:
                    if not perfil:
                        perfil = Transportista.objects.create(usuario=user)

                    vehiculo_anterior = perfil.vehiculo

                    if vehiculo_anterior and vehiculo_anterior != nuevo_vehiculo:
                        vehiculo_anterior.estado = EstadoVehiculo.DISPONIBLE
                        vehiculo_anterior.save(update_fields=["estado"])

                    perfil.vehiculo = nuevo_vehiculo
                    perfil.save(update_fields=["vehiculo"])

                    if nuevo_vehiculo:
                        nuevo_vehiculo.estado = EstadoVehiculo.ASIGNADO
                        nuevo_vehiculo.save(update_fields=["estado"])

                else:
                    if perfil:
                        if perfil.vehiculo:
                            perfil.vehiculo.estado = EstadoVehiculo.DISPONIBLE
                            perfil.vehiculo.save(update_fields=["estado"])
                        perfil.delete()

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
