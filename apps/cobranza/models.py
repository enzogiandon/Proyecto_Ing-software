# cobranza/models.py

from decimal import Decimal

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
    observacion = models.TextField(
        blank=True,
        null=True,
        help_text="Motivo documentado por el administrativo para no aprobar la cobranza",
    )
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"Cobranza Parada #{self.parada.id} - {self.parada.comercio.razon_social}"
        )

    def actualizar_tras_ajuste(self):
        """
        Recalcula el estado de la cobranza tras registrar un ajuste.
        No sobreescribe la observación inicial de validación/rechazo.
        """
        detalles = self.detalles.all()
        ajustes = self.ajustes.all()
        remitos = self.parada.remitos.filter(eliminado=False)

        total_declarado = sum(r.total for r in remitos)
        total_verificado_detalles = sum(
            d.monto_verificado for d in detalles if d.monto_verificado is not None
        )
        total_ajustes = sum(a.monto for a in ajustes)
        total_verificado = total_verificado_detalles + total_ajustes

        if total_declarado == total_verificado:
            self.estado = EstadoCobranza.APROBADO
        else:
            self.estado = EstadoCobranza.DIFIERE

        self.save(update_fields=["estado"])


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
        default=Decimal("0.00"),
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
    cobranza = models.ForeignKey(
        Cobranza,
        on_delete=models.CASCADE,
        related_name="ajustes",
        help_text="Cobranza sobre la cual se aplica el ajuste",
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        help_text="Administrativo que autorizó el ajuste",
    )
    medio = models.CharField(
        max_length=20,
        choices=MedioPago.choices,
        help_text="Medio de pago afectado por el ajuste",
    )
    monto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Monto del ajuste (positivo o negativo) se va a sumar al total de la cobranza",
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
        return f"Ajuste - {self.get_medio_display()}: ${self.monto}"
