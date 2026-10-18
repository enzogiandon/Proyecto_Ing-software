# itinerarios/models.py

from django.db import models

from config import settings

# Create your models here.

class DetalleRutaGuardada(models.Model):
    ruta_guardada = models.ForeignKey('RutaGuardada', on_delete=models.CASCADE)
    comercio = models.ForeignKey('remitos.Comercio', on_delete=models.CASCADE)
    prioridad = models.IntegerField(default=0)

    class Meta:
        ordering = ('-prioridad')

class RutaGuardada(models.Model):
    transportista = models.ForeignKey('core.Transportista', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    comercios = models.ManyToManyField('remitos.Comercio', through='DetalleRutaGuardada', related_name='rutas_guardadas')

    def __str__(self):
        return f"{self.nombre} - Transportista: {self.transportista}"

class Itinerario(models.Model):
    class EstadoItinerario(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        ASIGNADO = "asignado", "Asignado"
        EN_RUTA = "en_ruta", "En ruta"
        FINALIZADO = "finalizado", "Finalizado"

    fecha = models.DateField(help_text="Fecha de la entrega")
    estado = models.CharField(max_length=20, choices=EstadoItinerario.choices, default=EstadoItinerario.PENDIENTE)
    transportista = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True, null=True, related_name="itinerarios")
    vehiculo = models.ForeignKey("flota.Vehiculo", on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        verbose_name = "Itinerario"
        verbose_name_plural = "Itinerarios"
        ordering = ("-fecha")
    
    def __str__(self):
        return f"Itinerario #{self.id} - {self.fecha} ({self.get_estado_display()})"

class Parada(models.Model):
    class EstadoParada(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        FINALIZADA = "finalizada", "Finalizada"
        ERROR = "error", "Error"

    itinerario = models.ForeignKey(Itinerario, on_delete=models.CASCADE, related_name="paradas")
    comercio = models.ForeignKey('remitos.Comercio', on_delete=models.CASCADE, related_name='paradas')
    orden = models.PositiveIntegerField(default=0)
    estado = models.CharField(max_length=20, choices=EstadoParada.choices, default=EstadoParada.PENDIENTE)

    class Meta:
        ordering = ("itinerario", "orden")

