# flota/models.py

from django.db import models


class EstadoVehiculo(models.TextChoices):
    DISPONIBLE = "disponible", "Disponible"
    ASIGNADO = "asignado", "Asignado"
    NO_OPERATIVO = "no_operativo", "No operativo"


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
