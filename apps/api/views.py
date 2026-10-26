from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import transaction
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.api.serializers import (
    DetalleParadaSerializer,
    GuardarRutaSerializer,
    ListaParadaSerializer,
    RutaGuardadaSerializer,
)
from apps.itinerarios.models import (
    DetalleRutaGuardada,
    EstadoItinerario,
    Itinerario,
    Parada,
    RutaGuardada,
)
from apps.itinerarios.services import ordenar_itinerario_segun_ruta

from .serializers import CrearRutaGuardadaSerializer, GroupSerializer, UserSerializer

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
    Endpoints de itinerarios y rutas contextualizados al transportista autenticado:
    - GET  /api/itinerarios/paradas/
    - GET  /api/itinerarios/rutas-guardadas
    - POST /api/itinerarios/crear-ruta/
    - POST /api/itinerarios/guardar-ruta/
    - POST /api/itinerarios/ordenar-por-ruta/
    """

    queryset = Itinerario.objects.all()
    permission_classes = [IsAuthenticated]

    def _get_itinerario_activo(self, request):
        """
        Recupera el itinerario en curso o asignado al transportista autenticado.
        """
        user = request.user
        if not hasattr(user, "perfil_transportista"):
            raise ValidationError(
                {
                    "detail": "El usuario autenticado no tiene asignado un perfil de transportista."
                }
            )

        itinerario = Itinerario.objects.filter(
            transportista=user.perfil_transportista,
            estado__in=[EstadoItinerario.ASIGNADO, EstadoItinerario.EN_RUTA],
        ).first()

        if not itinerario:
            raise ValidationError(
                {
                    "detail": "No posees ningún itinerario activo o asignado en este momento."
                }
            )

        return itinerario

    @action(detail=False, methods=["get"], url_path="paradas")
    def paradas(self, request):
        """
        Devuelve la lista ordenada de paradas del chofer logueado.
        Endpoint: GET /api/itinerarios/paradas/
        """
        itinerario = self._get_itinerario_activo(request)
        paradas = (
            itinerario.paradas
            .select_related("comercio", "cobranza")
            .prefetch_related(
                "remitos__items",
                "cobranza__detalles",
            )
            .order_by("orden")
        )
        serializer = ListaParadaSerializer(paradas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="guardar-ruta")
    def guardar_ruta(self, request):
        """
        Persiste el nuevo orden de paradas para el itinerario activo en curso.
        Endpoint: POST /api/itinerarios/guardar-ruta/
        Body: {"parada_ids": [3, 1, 2]}
        """
        itinerario = self._get_itinerario_activo(request)
        serializer = GuardarRutaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        parada_ids = serializer.validated_data["parada_ids"]
        paradas_actuales = {p.id: p for p in itinerario.paradas.all()}

        if set(parada_ids) != set(paradas_actuales.keys()):
            raise ValidationError(
                {
                    "detail": "La lista enviada no coincide exactamente con las paradas del itinerario."
                }
            )

        paradas_para_actualizar = []
        for index, p_id in enumerate(parada_ids, start=1):
            parada = paradas_actuales[p_id]
            parada.orden = index
            paradas_para_actualizar.append(parada)

        with transaction.atomic():
            Parada.objects.bulk_update(paradas_para_actualizar, fields=["orden"])

        respuesta = ListaParadaSerializer(paradas_para_actualizar, many=True)
        return Response(respuesta.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="crear-ruta")
    def crear_ruta(self, request):
        """Crea o actualiza una plantilla de RutaGuardada vinculada al transportista en sesión

        y actualiza los comercios asociados con su prioridad correspondiente.
        Endpoint: POST /api/itinerarios/crear-ruta/
        Body: {
            "nombre": "Ruta Lluvias",
            "parada_ids": [3, 1, 2]
        }
        """
        itinerario = self._get_itinerario_activo(request)
        serializer = CrearRutaGuardadaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        nombre_ruta = serializer.validated_data["nombre"].strip()
        parada_ids = serializer.validated_data["parada_ids"]

        # Validar que las paradas pertenezcan al itinerario actual
        paradas_dict = {
            p.id: p for p in itinerario.paradas.select_related("comercio")
        }
        if not set(parada_ids).issubset(set(paradas_dict.keys())):
            raise ValidationError({
                "detail": (
                    "Algunas de las paradas indicadas no pertenecen a tu"
                    " itinerario activo."
                )
            })

        transportista = request.user.perfil_transportista

        with transaction.atomic():
            # 1. Obtenemos o creamos la cabecera de la ruta
            ruta_guardada, creada = RutaGuardada.objects.get_or_create(
                transportista=transportista,
                nombre=nombre_ruta,
            )

            # 2. Si ya existía, removemos los comercios previos para reemplazarlos por los nuevos
            if not creada:
                ruta_guardada.detalles.all().delete()

            # 3. Insertamos los nuevos detalles ordenados por prioridad
            detalles_para_crear = [
                DetalleRutaGuardada(
                    ruta_guardada=ruta_guardada,
                    comercio=paradas_dict[p_id].comercio,
                    prioridad=prioridad,
                )
                for prioridad, p_id in enumerate(parada_ids, start=1)
            ]

            DetalleRutaGuardada.objects.bulk_create(detalles_para_crear)

            ordenar_itinerario_segun_ruta(itinerario, ruta_guardada)

        status_code = (
            status.HTTP_201_CREATED if creada else status.HTTP_200_OK
        )
        mensaje = (
            "Ruta guardada exitosamente."
            if creada
            else "Ruta actualizada exitosamente."
        )

        return Response(
            {
                "id": ruta_guardada.id,
                "nombre": ruta_guardada.nombre,
                "total_comercios": len(detalles_para_crear),
                "actualizada": not creada,
                "mensaje": mensaje,
            },
            status=status_code,
        )

    @action(detail=False, methods=["get"], url_path="rutas-guardadas")
    def listar_rutas_guardadas(self, request):
      """
      Devuelve solo el id y el nombre de las rutas guardadas del transportista. Endpoint: GET /api/itinerarios/rutas-guardadas/
      """
      user = request.user
      if not hasattr(user, "perfil_transportista"):
        raise ValidationError({
            "detail": "El usuario autenticado no posee perfil de transportista."
        })

      rutas = RutaGuardada.objects.filter(
          transportista=user.perfil_transportista
      ).order_by("nombre")
      serializer = RutaGuardadaSerializer(rutas, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="ordenar-por-ruta")
    def ordenar_por_ruta(self, request):
        """
        Recibe {"ruta_id": <id>} y devuelve únicamente la lista de IDs de paradas ordenadas.
        Endpoint: POST /api/itinerarios/ordenar-por-ruta/
        """
        ruta_id = request.data.get("ruta_id")
        if not ruta_id:
            raise ValidationError({"ruta_id": "El campo 'ruta_id' es obligatorio."})

        # 1. Obtenemos el itinerario en curso del chofer logueado
        itinerario = self._get_itinerario_activo(request)
        transportista = request.user.perfil_transportista

        # 2. Verificamos que la plantilla pertenezca a este chofer
        try:
            ruta_guardada = RutaGuardada.objects.get(id=ruta_id, transportista=transportista)
        except RutaGuardada.DoesNotExist:
            raise NotFound({"detail": "La ruta enviada no existe o no pertenece a tu usuario."})

        # 3. Ejecutamos la función de ordenamiento que definiste
        paradas_ordenadas = ordenar_itinerario_segun_ruta(itinerario, ruta_guardada)

        # 4. Extraemos y retornamos exclusivamente las IDs ordenadas
        parada_ids_ordenadas = [parada.id for parada in paradas_ordenadas]
        return Response(parada_ids_ordenadas, status=status.HTTP_200_OK)


class ParadaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoints de paradas:
    - GET /api/paradas/{id}/ (Detalle con comercio y remitos asociados)
    """

    queryset = Parada.objects.select_related("comercio").prefetch_related("remitos")
    serializer_class = DetalleParadaSerializer
    permission_classes = [IsAuthenticated]
