# itinerarios/models.py

from django.db import models


class EstadoItinerario(models.TextChoices):
    PENDIENTE = "pendiente", "Pendiente"
    ASIGNADO = "asignado", "Asignado"
    FINALIZADO = "finalizado", "Finalizado"


class EstadoParada(models.TextChoices):
    PENDIENTE = "pendiente", "Pendiente"
    FINALIZADA = "finalizada", "Finalizada"
    ERROR = "error", "Error"
    RESUELTO = "resuelto", "Resuelto"


class TipoProblema(models.TextChoices):
    LOCAL_CERRADO = "local_cerrado", "Local cerrado"
    CLIENTE_AUSENTE = "cliente_ausente", "Cliente ausente"
    CLIENTE_RECHAZA_PEDIDO = "cliente_rechaza_pedido", "Cliente rechaza el pedido"
    DIRECCION_INCORRECTA  = "direccion_incorrecta", "Dirección incorrecta"
    PROBLEMA_PAGO = "problema_pago", "Problemas con el pago"
    MERCADERIA_DANADA = "mercaderia_danada", "Mercadería dañada"
    INACCESIBLE = "inaccesible", "Inaccesible"
    PROBLEMA_VEHICULO = "problema_vehiculo", "Problemas con el vehículo"
    OTRO = "otro", "Otro problema"


class DetalleRutaGuardada(models.Model):
    ruta_guardada = models.ForeignKey(
        "RutaGuardada", on_delete=models.CASCADE, related_name="detalles"
    )
    comercio = models.ForeignKey("remitos.Comercio", on_delete=models.CASCADE)
    prioridad = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = (models.F("prioridad").asc(nulls_last=True),)
        constraints = [
            models.UniqueConstraint(
                fields=["ruta_guardada", "comercio"], name="unique_comercio"
            )
        ]


class RutaGuardada(models.Model):
    transportista = models.ForeignKey("core.Transportista", on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    comercios = models.ManyToManyField(
        "remitos.Comercio",
        through="DetalleRutaGuardada",
        related_name="rutas_guardadas",
    )

    def __str__(self):
        return f"{self.nombre} - Transportista: {self.transportista}"


class Itinerario(models.Model):
    fecha = models.DateField(help_text="Fecha de la entrega")
    estado = models.CharField(
        max_length=20,
        choices=EstadoItinerario.choices,
        default=EstadoItinerario.PENDIENTE,
    )
    transportista = models.ForeignKey(
        "core.transportista",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="itinerarios",
    )
    vehiculo = models.ForeignKey(
        "core.Vehiculo", on_delete=models.PROTECT, blank=True, null=True
    )

    class Meta:
        verbose_name = "Itinerario"
        verbose_name_plural = "Itinerarios"
        ordering = ("-fecha",)

    def __str__(self):
        transportista = (
            self.transportista.usuario.get_full_name()
            or self.transportista.usuario.username
            if self.transportista
            else "Sin transportista"
        )
        return f"Itinerario #{self.id} - {transportista} - {self.fecha}"


class Parada(models.Model):
    itinerario = models.ForeignKey(
        Itinerario, on_delete=models.CASCADE, related_name="paradas"
    )
    comercio = models.ForeignKey(
        "remitos.Comercio", on_delete=models.CASCADE, related_name="paradas"
    )
    orden = models.PositiveIntegerField(default=0)
    estado = models.CharField(
        max_length=20, choices=EstadoParada.choices, default=EstadoParada.PENDIENTE
    )
    hora_entrega = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = (
            "-itinerario",
            "orden",
        )


class EvidenciaParada(models.Model):
    parada = models.ForeignKey(
        Parada, on_delete=models.CASCADE, related_name="evidencias"
    )
    archivo = models.ImageField(upload_to="remitos_firmados/")
    fecha = models.DateTimeField( auto_now_add=True)

    class Meta:
        verbose_name = "Evidencia de entrega"
        verbose_name_plural = "Evidencia de entregas"

    def __str__(self):
        return f"evidencia #{self.id} para la entrega #{self.parada.id}"


class ProblemaParada(models.Model):
    parada = models.ForeignKey(
        Parada,
        on_delete=models.CASCADE,
        related_name="problemas",
        help_text="Parada donde ocurrio el problema",
    )
    tipo = models.CharField(
        max_length=30, choices=TipoProblema.choices, default=TipoProblema.OTRO
    )
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    impide_entrega = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Problema en parada"
        verbose_name_plural = "Problemas en parada"
        ordering = ("-fecha",)

    def __str__(self):
        return f"Problema [{self.get_tipo_display()}] - Parada #{self.parada.id} ({self.parada.comercio.razon_social})"
