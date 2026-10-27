# core/models.py

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from simple_history.models import HistoricalRecords


class Roles(models.TextChoices):
    ADMINISTRATIVO = "administrativo", "Administrativo"
    TRANSPORTISTA = "transportista", "Transportista"
    ADMINISTRADOR = "administrador", "Administrador"


class EstadoVehiculo(models.TextChoices):
    DISPONIBLE = "disponible", "Disponible"
    ASIGNADO = "asignado", "Asignado"
    NO_OPERATIVO = "no_operativo", "No operativo"


class Usuario(AbstractUser):
    username = models.CharField(
        max_length=8,
        unique=True,
        validators=[
            RegexValidator(
                r"^\d{7,8}$",
                "El DNI debe contener 7 u 8 dígitos sin puntos ni guiones.",
            )
        ],
        help_text="Requerido. Ingrese el DNI (7 u 8 dígitos numéricos).",
        error_messages={
            "unique": "Ya existe un usuario registrado con este DNI.",
        },
    )
    telefono = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r"^\+?[\d\s\-()]{7,20}$",
                message="El número de teléfono debe ingresarse en un formato válido (ej: 54 9 11 1234 5678 o 1112345678).",
            )
        ],
        blank=True,
        null=True,
    )
    intentos_fallidos = models.IntegerField(default=0)
    rol = models.CharField(
        max_length=20, choices=Roles.choices, default=Roles.TRANSPORTISTA
    )
    history = HistoricalRecords()


class Vehiculo(models.Model):
    patente = models.CharField(
        max_length=7,
        unique=True,
        help_text="Patente del vehiculo (ej: AB123CD o ABC123",
    )

    modelo = models.CharField(
        max_length=50, blank=True, null=True, help_text="Marca y modelo del camión"
    )
    poliza = models.CharField(
        max_length=20, blank=True, null=True, help_text="Numero de poliza de seguro"
    )
    estado = models.CharField(
        max_length=20,
        choices=EstadoVehiculo.choices,
        default=EstadoVehiculo.DISPONIBLE,
        help_text="Estado operativo para la planificacion de rutas",
    )

    def __str__(self):
        return self.patente

    class Meta:
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"


class Transportista(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perfil_transportista",
    )
    vehiculo = models.ForeignKey(
        Vehiculo, on_delete=models.CASCADE, blank=True, null=True
    )
    history = HistoricalRecords()

    def __str__(self):
        return self.usuario.get_full_name() or self.usuario.username
