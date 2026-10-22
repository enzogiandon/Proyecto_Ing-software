from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import transaction
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.api.serializers import (
    DetalleParadaSerializer,
    GuardarRutaSerializer,
    ListaParadaSerializer,
)
from apps.itinerarios.models import Itinerario, Parada

from .serializers import GroupSerializer, UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all().order_by("name")
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class ItinerarioViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoints relacionados al itinerario:
    - GET  /api/itinerarios/{id}/paradas/
    - POST /api/itinerarios/{id}/guardar-ruta/
    """

    queryset = Itinerario.objects.all()
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["get"], url_path="paradas")
    def paradas(self, request, pk=None):
        """Devuelve las paradas de este itinerario ordenadas por 'orden'."""
        itinerario = self.get_object()
        paradas = itinerario.paradas.select_related("comercio").order_by("orden")
        serializer = ListaParadaSerializer(paradas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="guardar-ruta")
    def guardar_ruta(self, request, pk=None):
        """Recibe una lista de IDs de paradas y persiste su nueva secuencia."""
        itinerario = self.get_object()
        serializer = GuardarRutaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        parada_ids = serializer.validated_data["parada_ids"]

        # Traemos todas las paradas que pertenecen a este itinerario
        paradas_actuales = {p.id: p for p in itinerario.paradas.all()}

        # Validamos que los IDs enviados coincidan con las paradas del itinerario
        if set(parada_ids) != set(paradas_actuales.keys()):
            raise ValidationError(
                "La lista de paradas enviada no coincide exactamente con las paradas del itinerario."
            )

        # Asignamos el nuevo orden según la posición en el array JSON
        paradas_para_actualizar = []
        for index, p_id in enumerate(parada_ids, start=1):
            parada = paradas_actuales[p_id]
            parada.orden = index
            paradas_para_actualizar.append(parada)

        with transaction.atomic():
            Parada.objects.bulk_update(paradas_para_actualizar, fields=["orden"])

        # Devolvemos la lista ya ordenada
        respuesta = ListaParadaSerializer(paradas_para_actualizar, many=True)
        return Response(respuesta.data, status=status.HTTP_200_OK)


class ParadaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoints de paradas:
    - GET /api/paradas/{id}/ (Detalle con comercio y remitos asociados)
    """

    queryset = Parada.objects.select_related("comercio").prefetch_related("remitos")
    serializer_class = DetalleParadaSerializer
    permission_classes = [IsAuthenticated]
