from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers

from apps.itinerarios import Itinerario, Parada
from apps.remitos import Comercio, Remito

User = get_user_model()


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
        fields = ["id", "razon_social", "cuit", "direccion", "telefono"]


class RemitoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Remito
        fields = ["id", "numero", "estado", "comercio"]


class ListaParadaSerializer(serializers.ModelSerializer):
    comercio = ComercioSerializer(read_only=True)

    class Meta:
        model = Parada
        fields = ["id", "itinerario", "orden", "estado", "comercio"]


class DetalleParadaSerializer(serializers.ModelSerializer):
    comercio = ComercioSerializer(read_only=True)
    remitos = RemitoSerializer(many=True, read_only=True)

    class Meta:
        model = Parada
        fields = ["id", "itinerario", "orden", "estado", "comercio", "remitos"]


class GuardarRutaSerializer(serializers.ModelSerializer):
    parada_ids = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=False,
        help_text="Lista de IDs de paradas el el orden deseado",
    )

