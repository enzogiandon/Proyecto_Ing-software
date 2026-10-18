# flota/models.py

from django.db import models

# Create your models here.


class Vehiculo(models.Model):
    class EstadoVehiculo(models.TextChoices):
        DISPONIBLE = "disponible", "Disponible"
        ASIGNADO = "asignado", "Asignado"
        NO_OPERATIVO = "no_operativo", "No operativo"

    patente = models.CharField(
        max_length=7,
        unique=True,
        help_text="Patente del vehiculo (ej: AB123CD o ABC123",
    )
    modelo = models.CharField(
        max_length=50, blank=True, null=True, help_text="Marca y modelo del camión"
    )
    estado = models.CharField(
        max_length=20,
        choices=EstadoVehiculo.choices,
        default=EstadoVehiculo.DISPONIBLE,
        help_text="Estado operativo para la planificacion de rutas",
    )

    class Meta:
        verbose_name = 'Vehículo'
        verbose_name_plural = "Vehículos"

    def __str__(self):
        return f"Camion {self.patente} ({self.get_estado_display()})"
