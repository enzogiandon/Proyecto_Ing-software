from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models import Sum
from rest_framework import serializers

from apps.cobranza.models import MedioPago
from apps.itinerarios.models import Parada, RutaGuardada
from apps.remitos.models import Comercio, Remito

User = get_user_model()


def calcular_monto_recaudar(parada) -> str:
    total_remitos = (
        parada.remitos.filter(eliminado=False).aggregate(
            total=Sum("total")
        )["total"]
        or Decimal("0.00")
    )
    total_pagado = Decimal("0.00")
    if hasattr(parada, "cobranza"):
        total_pagado = (
            parada.cobranza.detalles.aggregate(
                total=Sum("monto_declarado")
            )["total"]
            or Decimal("0.00")
        )

    # 3. Saldo pendiente a cobrar (no menor a 0)
    saldo_pendiente = max(Decimal("0.00"), total_remitos - total_pagado)
    return str(round(saldo_pendiente, 2))


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "groups"]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class ComercioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comercio
        fields = ["id", "razon_social", "cuit", "domicilio", "telefono"]


class RemitoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Remito
        fields = ["id", "numero", "estado", "comercio", "total"]


class ListaParadaSerializer(serializers.ModelSerializer):
    comercio = ComercioSerializer(read_only=True)
    monto_recaudar = serializers.SerializerMethodField()

    class Meta:
        model = Parada
        fields = ["id", "orden", "estado", "comercio", "monto_recaudar"]

    def get_monto_recaudar(self, obj) -> str:
        return calcular_monto_recaudar(obj)


class DetalleParadaSerializer(serializers.ModelSerializer):
    comercio = ComercioSerializer(read_only=True)
    remitos = RemitoSerializer(many=True, read_only=True)
    monto_recaudar = serializers.SerializerMethodField()

    class Meta:
        model = Parada
        fields = ["id", "itinerario", "orden", "estado", "comercio", "remitos", "monto_recaudar"]

    def get_monto_recaudar(self, obj) -> str:
        return calcular_monto_recaudar(obj)


class GuardarRutaSerializer(serializers.Serializer):
    parada_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        help_text="Lista de IDs de paradas el el orden deseado",
    )


class CrearRutaGuardadaSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=50, required=True)
    # Lista de IDs de parada en el orden deseado para guardar la plantilla
    parada_ids = serializers.ListField(
        child=serializers.IntegerField(), required=True, allow_empty=False
    )


class RutaGuardadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RutaGuardada
        fields = ["id", "nombre"]


class RegistrarPagoInputSerializer(serializers.Serializer):
    medio = serializers.ChoiceField(choices=MedioPago.choices)
    monto = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal("0.01"),
    )
