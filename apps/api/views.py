from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import parsers, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.api.serializers import (
    DetalleParadaSerializer,
    EvidenciaParadaSerializer,
    GuardarRutaSerializer,
    ListaParadaSerializer,
    ProblemaParadaSerializer,
    RegistrarPagoInputSerializer,
    RegistrarProblemaInputSerializer,
    RutaGuardadaSerializer,
)
from apps.cobranza.models import Cobranza, DetallePago, EstadoCobranza
from apps.itinerarios.models import (
    DetalleRutaGuardada,
    EstadoItinerario,
    EstadoParada,
    EvidenciaParada,
    Itinerario,
    Parada,
    ProblemaParada,
    RutaGuardada,
)
from apps.itinerarios.services import ordenar_itinerario_segun_ruta
from apps.remitos.models import EstadoRemito

from .serializers import (
    CrearRutaGuardadaSerializer,
)

User = get_user_model()


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
            estado__in=[EstadoItinerario.ASIGNADO],
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
            itinerario.paradas.select_related("comercio", "cobranza")
            .prefetch_related(
                "remitos",
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
        paradas_dict = {p.id: p for p in itinerario.paradas.select_related("comercio")}
        if not set(parada_ids).issubset(set(paradas_dict.keys())):
            raise ValidationError(
                {
                    "detail": (
                        "Algunas de las paradas indicadas no pertenecen a tu"
                        " itinerario activo."
                    )
                }
            )

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

        status_code = status.HTTP_201_CREATED if creada else status.HTTP_200_OK
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
            raise ValidationError(
                {"detail": "El usuario autenticado no posee perfil de transportista."}
            )

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
            ruta_guardada = RutaGuardada.objects.get(
                id=ruta_id, transportista=transportista
            )
        except RutaGuardada.DoesNotExist:
            raise NotFound(
                {"detail": "La ruta enviada no existe o no pertenece a tu usuario."}
            )

        # 3. Ejecutamos la función de ordenamiento que definiste
        paradas_ordenadas = ordenar_itinerario_segun_ruta(itinerario, ruta_guardada)

        # 4. Extraemos y retornamos exclusivamente las IDs ordenadas
        parada_ids_ordenadas = [parada.id for parada in paradas_ordenadas]
        return Response(parada_ids_ordenadas, status=status.HTTP_200_OK)


class ParadaViewSet(viewsets.ModelViewSet):
    queryset = Parada.objects.select_related("comercio", "cobranza").prefetch_related(
        "remitos"
    )
    serializer_class = DetalleParadaSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["post"], url_path="registrar-cobranza")
    def registrar_cobranza(self, request, pk=None):
        """
        POST /api/paradas/{id}/registrar-cobranza/
        Body:
        [
            {"medio": "qr", "monto": 100.00},
            {"medio": "efectivo", "monto": 100.00}
        ]
        """
        parada = self.get_object()
        remitos = parada.remitos

        if not isinstance(request.data, list) or len(request.data) == 0:
            raise ValidationError(
                "Se espera una lista con al menos un detalle de pago."
            )

        serializer = RegistrarPagoInputSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        pagos_validados = serializer.validated_data

        with transaction.atomic():
            cobranza, _ = Cobranza.objects.get_or_create(
                parada=parada,
                defaults={"estado": EstadoCobranza.REGISTRADO},
            )

            detalles_a_crear = [
                DetallePago(
                    cobranza=cobranza,
                    medio=pago["medio"],
                    monto_declarado=pago["monto"],
                )
                for pago in pagos_validados
            ]

            DetallePago.objects.bulk_create(detalles_a_crear)

            parada.remitos.filter(eliminado=False).update(estado=EstadoRemito.ENTREGADO)

            parada.estado = EstadoParada.FINALIZADA
            parada.save(update_fields=["estado"])

            # 4. Validar si era la última parada pendiente del itinerario
            itinerario = parada.itinerario
            quedan_paradas_pendientes = (
                itinerario.paradas.exclude(id=parada.id)
                .exclude(estado=EstadoParada.FINALIZADA)
                .exists()
            )

            itinerario_finalizado = False
            if not quedan_paradas_pendientes:
                itinerario.estado = EstadoItinerario.FINALIZADO
                itinerario.save(update_fields=["estado"])
                itinerario_finalizado = True

        return Response(
            {
                "mensaje": "Cobranza y pagos registrados correctamente.",
                "cobranza_id": cobranza.id,
                "pagos_registrados": len(detalles_a_crear),
                "parada_estado": parada.estado,
                "itinerario_finalizado": itinerario_finalizado,
            },
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=["post"], url_path="reportar-problema")
    def reportar_problema(self, request, pk=None):
        parada = self.get_object()

        serializer = RegistrarProblemaInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tipo = serializer.validated_data["tipo"]
        descripcion = serializer.validated_data.get("descripcion", "")
        impide_entrega = serializer.validated_data["impide_entrega"]

        with transaction.atomic():
            problema = ProblemaParada.objects.create(
                parada=parada,
                tipo=tipo,
                descripcion=descripcion,
                impide_entrega=impide_entrega,
            )

            # Si impide la entrega, la parada pasa a estado ERROR
            if impide_entrega:
                parada.estado = EstadoParada.ERROR
                parada.save(update_fields=["estado"])

            # Validar si el itinerario queda completamente finalizado
            itinerario = parada.itinerario
            quedan_pendientes = (
                itinerario.paradas.exclude(id=parada.id)
                .filter(estado=EstadoParada.PENDIENTE)
                .exists()
            )

            itinerario_finalizado = False
            if not quedan_pendientes and parada.estado != EstadoParada.PENDIENTE:
                itinerario.estado = EstadoItinerario.FINALIZADO
                itinerario.save(update_fields=["estado"])
                itinerario_finalizado = True

        return Response(
            {
                "mensaje": "Problema registrado correctamente.",
                "problema": ProblemaParadaSerializer(problema).data,
                "parada_estado": parada.estado,
                "itinerario_finalizado": itinerario_finalizado,
            },
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="subir-evidencia",
        parser_classes=[parsers.MultiPartParser, parsers.FormParser],
    )
    def subir_evidencia(self, request, pk=None):
        """
        POST /api/paradas/{id}/subir-evidencia/
        multipart/form-data:
          archivo: <archivo binario>
        """
        parada = self.get_object()

        if "archivo" not in request.FILES:
            raise ValidationError(
                {
                    "archivo": "No se envió ningún archivo de imagen en el campo 'archivo'."
                }
            )

        archivo = request.FILES["archivo"]
        evidencia = EvidenciaParada.objects.create(
            parada=parada,
            archivo=archivo,
        )

        serializer = EvidenciaParadaSerializer(evidencia, context={"request": request})
        return Response(
            {
                "mensaje": "Evidencia subida correctamente.",
                "evidencia": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )
