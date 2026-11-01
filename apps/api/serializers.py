from decimal import Decimal

from django.contrib.auth import authenticate, get_user_model
from django.db.models import Sum
from rest_framework import exceptions, serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.cobranza.models import MedioPago
from apps.itinerarios.models import (
    EvidenciaParada,
    Parada,
    ProblemaParada,
    RutaGuardada,
    TipoProblema,
)
from apps.remitos.models import Comercio, Remito

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get(self.username_field)
        password = attrs.get("password")

        try:
            user = User.objects.get(**{self.username_field: username})
        except User.DoesNotExist:
            raise AuthenticationFailed("Credenciales inválidas.")


        if user and user.check_password(password) and not user.is_active:
            raise exceptions.AuthenticationFailed(
                {
                    "detail": "Tu cuenta se encuentra suspendida. Contacta al administrador.",
                    "codigo": "CUENTA_SUSPENDIDA",
                }
            )

        authenticated_user = authenticate(username=username, password=password)

        if not authenticated_user:
            user.intentos_fallidos += 1
            if user.intentos_fallidos >= 5:
                user.is_active = False
                user.save(update_fields=['intentos_fallidos', 'is_active'])
                raise AuthenticationFailed("Superaste el límite de intentos. Cuenta bloqueada.")

            user.save(update_fields=['intentos_fallidos'])
            raise AuthenticationFailed("Contraseña incorrecta.")

        if user.intentos_fallidos > 0:
            user.intentos_fallidos = 0
            user.save(update_fields=['intentos_fallidos'])

        return super().validate(attrs)


def calcular_monto_recaudar(parada) -> str:
    total_remitos = parada.remitos.filter(eliminado=False).aggregate(
        total=Sum("total")
    )["total"] or Decimal("0.00")
    total_pagado = Decimal("0.00")
    if hasattr(parada, "cobranza"):
        total_pagado = parada.cobranza.detalles.aggregate(total=Sum("monto_declarado"))[
            "total"
        ] or Decimal("0.00")

    # 3. Saldo pendiente a cobrar (no menor a 0)
    saldo_pendiente = max(Decimal("0.00"), total_remitos - total_pagado)
    return str(round(saldo_pendiente, 2))


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


class ProblemaParadaSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source="get_tipo_display", read_only=True)

    class Meta:
        model = ProblemaParada
        fields = [
            "id",
            "parada",
            "tipo",
            "tipo_display",
            "descripcion",
            "impide_entrega",
            "fecha",
        ]
        read_only_fields = ["id", "parada", "fecha"]


class EvidenciaParadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvidenciaParada
        fields = ["id", "parada", "archivo", "fecha"]
        read_only_fields = ["id", "parada", "fecha"]


class DetalleParadaSerializer(serializers.ModelSerializer):
    comercio = ComercioSerializer(read_only=True)
    remitos = RemitoSerializer(many=True, read_only=True)
    monto_recaudar = serializers.SerializerMethodField()
    evidencias = EvidenciaParadaSerializer(many=True, read_only=True)

    class Meta:
        model = Parada
        fields = [
            "id",
            "itinerario",
            "orden",
            "estado",
            "comercio",
            "remitos",
            "monto_recaudar",
            "evidencias",
        ]

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


class RegistrarProblemaInputSerializer(serializers.Serializer):
    tipo = serializers.ChoiceField(
        choices=TipoProblema.choices,
        default=TipoProblema.OTRO,
    )
    descripcion = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
        allow_null=True,
        default="",
    )
    impide_entrega = serializers.BooleanField(default=False)

    def validate(self, attrs):
        tipo = attrs.get("tipo")
        descripcion = (attrs.get("descripcion") or "").strip()

        # Si el tipo es 'otro', la descripción es obligatoria
        if tipo == TipoProblema.OTRO and not descripcion:
            raise serializers.ValidationError(
                {
                    "descripcion": "Debe proporcionar una descripción cuando el tipo de problema es 'Otro'."
                }
            )

        attrs["descripcion"] = descripcion
        return attrs
