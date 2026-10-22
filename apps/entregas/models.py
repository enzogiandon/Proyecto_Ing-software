# entregas/models.py

from django.db import models


class Entrega(models.Model):
    parada = models.OneToOneField('itinerarios.Parada', on_delete=models.CASCADE, related_name="entrega")
    hora_recepcion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Entrega"
        verbose_name_plural = "Entregas"

    def __str__(self):
        return f"Entregar realizada por {self.transportista.name} en {self.parada.comercio.nombre}"

class EvidenciaEntrega(models.Model):
    entrega = models.ForeignKey(Entrega, on_delete=models.CASCADE, related_name='evidencias')
    archivo = models.ImageField(upload_to='remitos_firmados/')
    fecha = models.DateTimeField(auto_now_add=True, help_text="Fecha en la que se subio la imagen")

    class Meta:
        verbose_name = "Evidencia de entrega"
        verbose_name_plural = "Evidencia de entregas"

    def __str__(self):
        return f"evidencia #{self.id} para la entrega #{self.entrega.id}"

class ProblemaEntrega(models.Model):
    class TipoProblema(models.TextChoices):
        MERCADERIA_DANADA = "mercaderia_danada", "Mercadería dañada o faltante"
        RECHAZO_PARCIAL = "rechazo_parcial", "Rechazo parcial"
        RECHAZO_TOTAL = "rechazo_total", "Rechazo total"
        OTRO = "otro", "Otro problema"

    parada = models.ForeignKey("itinerarios.Parada", on_delete=models.CASCADE, related_name="problemas", help_text="Parada donde ocurrio el problema")
    remito = models.ForeignKey("remitos.Remito", on_delete=models.PROTECT, blank=True, null=True, related_name="problemas")
    tipo = models.CharField(max_length=30, choices=TipoProblema.choices, default=TipoProblema.OTRO)
    imagen = models.ImageField(upload_to='problemas_entregas/', blank=True, null=True, help_text="Foto de la mercaderia dañada")
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Problema en parada"
        verbose_name_plural = "Problemas en paradas"
        ordering = ('-fecha',)

    def __str__(self):
        return f"Problema [{self.get_tipo_display()}] - Parada #{self.parada.id} ({self.parada.comercio.nombre})"
