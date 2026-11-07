# cobranza/models.py

from django.conf import settings
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
        return (
            f"Cobranza Parada #{self.parada.id} - {self.parada.comercio.razon_social}"
        )


class DetallePago(models.Model):
    cobranza = models.ForeignKey(
        Cobranza, on_delete=models.CASCADE, related_name="detalles"
    )
    medio = models.CharField(max_length=20, choices=MedioPago.choices)
    monto_declarado = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Importe informado por el transportista",
    )
    monto_verificado = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Importe verificado por el administrativo",
    )

    # Identificadores de Mercado Pago
    mp_preference_id = models.CharField(max_length=100, blank=True, null=True)
    mp_payment_id = models.CharField(max_length=100, blank=True, null=True, unique=True)

    class Meta:
        verbose_name = "Detalle del pago"
        verbose_name_plural = "Detalles de pagos"

    def __str__(self):
        return f"{self.get_medio_display()} - Declarado: ${self.monto_declarado}"


class AjusteCobranza(models.Model):
    detalle_pago = models.ForeignKey(
        DetallePago,
        on_delete=models.CASCADE,
        related_name="ajustes",
        help_text="Detalle de pago puntual sobre el cual se aplica la corrección",
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        help_text="Administrativo que autorizó el ajuste",
    )
    importe_anterior = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Monto verificado antes de aplicar el ajuste (o declarado si estaba sin verificar)",
    )
    importe_nuevo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Monto corregido final determinado por el administrativo",
    )
    motivo = models.TextField(
        help_text="Justificación obligatoria del ajuste",
    )
    fecha = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora exacta en que se registró el ajuste",
    )

    class Meta:
        verbose_name = "Ajuste de cobranza"
        verbose_name_plural = "Ajustes de cobranzas"
        ordering = ["-fecha"]

    def __str__(self):
        return f"Ajuste {self.detalle_pago.get_medio_display()} (#{self.detalle_pago.id}): ${self.importe_anterior} -> ${self.importe_nuevo}"
