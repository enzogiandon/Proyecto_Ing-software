# cobranza/models.py

from django.db import models


class MedioPago(models.TextChoices):
    EFECTIVO = "efectivo", "Efectivo"
    TRANSFERENCIA = "transferencia", "Transferencia"
    QR = "qr", "QR"


class EstadoCobranza(models.TextChoices):
    REGISTRADO = "registrado", "Registrado"
    APROBADO = "aprobado", "Aprobado"
    DIFIERE = "difiere", "Difiere"
    NO_ENCONTRADO = "no_encontrado", "No encontrado"


class Cobranza(models.Model):
    parada = models.OneToOneField(
        "itinerarios.Parada",
        on_delete=models.PROTECT,
        related_name="cobranza",
        help_text="Parada donde se efectuo la cobranza",
    )
    estado = models.CharField(
        max_length=20,
        choices=EstadoCobranza.choices,
        default=EstadoCobranza.REGISTRADO,
        help_text="Estado de validación despues de hacer el arqueo y revisión de movimientos",
    )
    observacion_ajuste = models.TextField(
        blank=True,
        null=True,
        help_text="Motivo documentado por el administrativo para no aprobar la cobranza",
    )
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comercio {self.parada.comercio.razon_social} ~~ "


class DetallePago(models.Model):
    cobranza = models.ForeignKey(
        Cobranza, on_delete=models.CASCADE, related_name="detalles"
    )
    medio = models.CharField(max_length=20, choices=MedioPago.choices)
    monto_declarado = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Imprte informado por el transportista",
    )
    monto_verificado = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Importe verificado por el administrativo",
    )
    cuenta_destino = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Cuenta a la que llego la transferencia",
    )

    class Meta:
        verbose_name = "Detalle del pago"
        verbose_name_plural = "Detalles de pagos"

    def __str__(self):
        return f"{self.get_medio_display()} - Declarado: ${self.monto_declarado} | Verificado ${self.monto_verificado}"
