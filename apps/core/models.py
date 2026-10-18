from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from simple_history.models import HistoricalRecords

phone_validator = RegexValidator(
    regex=r'^\+?[\d\s\-()]{7,20}$',
    message="El número de teléfono debe ingresarse en un formato válido (ej: +54 9 11 1234-5678 o 1112345678)."
)

class Usuario(AbstractUser):
    telefono = models.CharField(max_length=20, validators=[phone_validator], blank=True, null=True)
    dni = models.CharField(
        max_length=8,
        unique=True,
        validators=[
            RegexValidator(
                r"^\d{7,8}$",
                "El DNI debe contener 7 u 8 dígitos sin puntos ni guiones.",
            )
        ],
    )
    intentos_fallidos = models.IntegerField(default=0)
    history = HistoricalRecords()


class CentroAcopio(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20, validators=[phone_validator], blank=True, null=True)
    activo = models.BooleanField(default=True)
    history = HistoricalRecords()


class Transportista(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perfil_transportista",
    )
    habilitado = models.BooleanField(default=True)
    centro = models.ForeignKey(CentroAcopio, on_delete=models.CASCADE, blank=True, null=True)
    vehiculo = models.ForeignKey('flota.Vehiculo', on_delete=models.CASCADE, blank=True, null=True)
    history = HistoricalRecords()
