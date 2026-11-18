# remitos/models.py

import os
import uuid

from django.core.validators import RegexValidator
from django.db import models


class EstadoImportacion(models.TextChoices):
    PENDIENTE = "pendiente", "Pendiente"
    EXITO = "exito", "Exito"
    RECHAZADO = "rechazado", "Rechazado"


class EstadoRemito(models.TextChoices):
    PENDIENTE = "pendiente", "Pendiente"
    ASIGNADO = "asignado", "Asignado"
    ENTREGADO = "entregado", "Entregado"
    RECHAZADO = "rechazado", "Rechazado"


class Marca(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    cuit = models.CharField(max_length=11, unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Comercio(models.Model):
    razon_social = models.CharField(max_length=100)
    cuit = models.CharField(
        max_length=11,
        validators=[
            RegexValidator(
                regex=r"^\d{11}$",
                message="El cuit debe tener 11 digitos sin puntos ni guiones",
            )
        ],
    )
    domicilio = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.razon_social} - {self.domicilio}"


def ruta_lote(instance, filename):
    nombre_base, extension = os.path.splitext(os.path.basename(filename))
    hash_sufijo = uuid.uuid4().hex[:8]
    nuevo_nombre = f"{nombre_base}_{hash_sufijo}{extension}"

    return os.path.join("importaciones", nuevo_nombre)


class ImportacionRemitos(models.Model):
    archivo = models.FileField(
        upload_to=ruta_lote, help_text="Planilla enviadas por la marca"
    )
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(
        default=0, help_text="Cantidad de remitos agregados por esta importacion"
    )
    estado = models.CharField(
        max_length=20,
        choices=EstadoImportacion.choices,
        default=EstadoImportacion.RECHAZADO,
    )
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Importacion"
        verbose_name_plural = "Importaciones"
        ordering = ("-fecha",)

    def __str__(self):
        return f"Lote #{self.id} - {self.marca.nombre} ({self.fecha.strftime('%d/%m/%Y %H:%M')})"


class ErrorImportacion(models.Model):
    importacion = models.ForeignKey(
        ImportacionRemitos, on_delete=models.CASCADE, related_name="errores"
    )
    fila = models.PositiveIntegerField()
    motivo = models.TextField(help_text="Descripcion del motivo del rechazo")

    class Meta:
        verbose_name = "Error de importacion"
        verbose_name_plural = "Errores de importacion"

    def __str__(self):
        return f"Fila {self.fila} (Lote: {self.importacion.id}"


class Remito(models.Model):
    numero = models.CharField(max_length=50, unique=True, help_text="Numero de remito")
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT, related_name="remitos")
    estado = models.CharField(
        max_length=20, choices=EstadoRemito.choices, default=EstadoRemito.PENDIENTE
    )
    parada = models.ForeignKey(
        "itinerarios.Parada",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="remitos",
    )
    comercio = models.ForeignKey(
        Comercio, on_delete=models.PROTECT, related_name="remitos"
    )
    total = models.DecimalField(max_digits=10, decimal_places=2)
    importacion = models.ForeignKey(
        ImportacionRemitos,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="remitos",
    )

    def __str__(self):
        return f"Remito #{self.numero} - {self.comercio.razon_social}"

