from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.api.views import ItinerarioViewSet, ParadaViewSet
from apps.cobranza.models import Cobranza
from apps.core.models import Transportista
from apps.itinerarios.models import (
    DetalleRutaGuardada,
    EstadoItinerario,
    EstadoParada,
    Itinerario,
    Parada,
    RutaGuardada,
)
from apps.remitos.models import Comercio, EstadoRemito, Marca, Remito

User = get_user_model()


class RegistrarCobranzaTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username="12345678", password="secret123")
        self.transportista = Transportista.objects.create(usuario=self.user)
        self.itinerario = Itinerario.objects.create(
            fecha=date.today(),
            estado=EstadoItinerario.ASIGNADO,
            transportista=self.transportista,
        )
        self.comercio = Comercio.objects.create(
            razon_social="Comercio Test",
            cuit="30112233445",
            domicilio="Calle Falsa 123",
        )
        self.marca = Marca.objects.create(
            nombre="Marca Test",
            cuit="30998877665",
            activo=True,
        )
        self.parada = Parada.objects.create(
            itinerario=self.itinerario,
            comercio=self.comercio,
            orden=1,
            estado=EstadoParada.PENDIENTE,
        )
        self.remito = Remito.objects.create(
            numero="R-001",
            marca=self.marca,
            comercio=self.comercio,
            total=Decimal("100.00"),
            estado=EstadoRemito.ASIGNADO,
            parada=self.parada,
        )

    def test_cobranza_parcial_no_cierra_la_visita(self):
        payload = [{"medio": "efectivo", "monto": "70.00"}]
        request = self.factory.post(
            f"/api/paradas/{self.parada.id}/registrar-cobranza/",
            payload,
            format="json",
        )
        force_authenticate(request, user=self.user)

        response = ParadaViewSet.as_view({"post": "registrar_cobranza"})(
            request,
            pk=self.parada.pk,
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(Cobranza.objects.filter(parada=self.parada).exists())

        self.parada.refresh_from_db()
        self.remito.refresh_from_db()
        self.assertEqual(self.parada.estado, EstadoParada.PENDIENTE)
        self.assertEqual(self.remito.estado, EstadoRemito.ASIGNADO)


class ItinerarioViewSetTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username="12345678", password="secret123")
        self.transportista = Transportista.objects.create(usuario=self.user)
        self.itinerario = Itinerario.objects.create(
            fecha=date.today(),
            estado=EstadoItinerario.ASIGNADO,
            transportista=self.transportista,
        )
        self.c1 = Comercio.objects.create(razon_social="Comercio 1", cuit="30111111111", domicilio="Calle 1")
        self.c2 = Comercio.objects.create(razon_social="Comercio 2", cuit="30222222222", domicilio="Calle 2")
        self.c3 = Comercio.objects.create(razon_social="Comercio 3", cuit="30333333333", domicilio="Calle 3")
        self.c4 = Comercio.objects.create(razon_social="Comercio 4", cuit="30444444444", domicilio="Calle 4")

        self.p1 = Parada.objects.create(itinerario=self.itinerario, comercio=self.c1, orden=1, estado=EstadoParada.FINALIZADA)
        self.p2 = Parada.objects.create(itinerario=self.itinerario, comercio=self.c2, orden=2, estado=EstadoParada.PENDIENTE)
        self.p3 = Parada.objects.create(itinerario=self.itinerario, comercio=self.c3, orden=3, estado=EstadoParada.PENDIENTE)
        self.p4 = Parada.objects.create(itinerario=self.itinerario, comercio=self.c4, orden=4, estado=EstadoParada.PENDIENTE)

    def test_guardar_ruta_reordenamiento_completo(self):
        payload = {"parada_ids": [self.p1.id, self.p4.id, self.p3.id, self.p2.id]}
        request = self.factory.post("/api/itinerarios/guardar-ruta/", payload, format="json")
        force_authenticate(request, user=self.user)
        response = ItinerarioViewSet.as_view({"post": "guardar_ruta"})(request)

        self.assertEqual(response.status_code, 200)
        self.p1.refresh_from_db()
        self.p4.refresh_from_db()
        self.p3.refresh_from_db()
        self.p2.refresh_from_db()
        self.assertEqual(self.p1.orden, 1)
        self.assertEqual(self.p4.orden, 2)
        self.assertEqual(self.p3.orden, 3)
        self.assertEqual(self.p2.orden, 4)

    def test_guardar_ruta_reordenamiento_parcial_preserva_paradas_finalizadas(self):
        # p1 (finalizada) no se incluye en el payload; solo se reordenan las pendientes p2, p3, p4
        payload = {"parada_ids": [self.p4.id, self.p2.id, self.p3.id]}
        request = self.factory.post("/api/itinerarios/guardar-ruta/", payload, format="json")
        force_authenticate(request, user=self.user)
        response = ItinerarioViewSet.as_view({"post": "guardar_ruta"})(request)

        self.assertEqual(response.status_code, 200)
        self.p1.refresh_from_db()
        self.p4.refresh_from_db()
        self.p2.refresh_from_db()
        self.p3.refresh_from_db()
        # p1 debe conservar inalterada su posición 1
        self.assertEqual(self.p1.orden, 1)
        # Las paradas pendientes deben ocupar los slots 2, 3, 4 en el orden solicitado
        self.assertEqual(self.p4.orden, 2)
        self.assertEqual(self.p2.orden, 3)
        self.assertEqual(self.p3.orden, 4)

    def test_guardar_ruta_rechaza_ids_duplicados(self):
        payload = {"parada_ids": [self.p2.id, self.p2.id, self.p3.id]}
        request = self.factory.post("/api/itinerarios/guardar-ruta/", payload, format="json")
        force_authenticate(request, user=self.user)
        response = ItinerarioViewSet.as_view({"post": "guardar_ruta"})(request)

        self.assertEqual(response.status_code, 400)
        self.assertIn("parada_ids", response.data)

    def test_guardar_ruta_rechaza_ids_ajenos(self):
        payload = {"parada_ids": [999999]}
        request = self.factory.post("/api/itinerarios/guardar-ruta/", payload, format="json")
        force_authenticate(request, user=self.user)
        response = ItinerarioViewSet.as_view({"post": "guardar_ruta"})(request)

        self.assertEqual(response.status_code, 400)

    def test_crear_ruta_sin_parada_ids_toma_orden_actual(self):
        payload = {"nombre": "Ruta Default"}
        request = self.factory.post("/api/itinerarios/crear-ruta/", payload, format="json")
        force_authenticate(request, user=self.user)
        response = ItinerarioViewSet.as_view({"post": "crear_ruta"})(request)

        self.assertEqual(response.status_code, 201)
        ruta = RutaGuardada.objects.get(nombre="Ruta Default")
        detalles = list(ruta.detalles.order_by("prioridad"))
        self.assertEqual(len(detalles), 4)
        self.assertEqual(detalles[0].comercio, self.c1)
        self.assertEqual(detalles[1].comercio, self.c2)

    def test_crear_ruta_rechaza_ids_duplicados(self):
        payload = {"nombre": "Ruta Dups", "parada_ids": [self.p2.id, self.p2.id]}
        request = self.factory.post("/api/itinerarios/crear-ruta/", payload, format="json")
        force_authenticate(request, user=self.user)
        response = ItinerarioViewSet.as_view({"post": "crear_ruta"})(request)

        self.assertEqual(response.status_code, 400)
        self.assertIn("parada_ids", response.data)

    def test_crear_ruta_rechaza_ids_invalidos(self):
        payload = {"nombre": "Ruta Invalida", "parada_ids": [999999]}
        request = self.factory.post("/api/itinerarios/crear-ruta/", payload, format="json")
        force_authenticate(request, user=self.user)
        response = ItinerarioViewSet.as_view({"post": "crear_ruta"})(request)

        self.assertEqual(response.status_code, 400)

    def test_crear_ruta_deduplica_por_comercio_sin_integrity_error(self):
        # Crear una quinta parada con comercio c1 repetido en el mismo itinerario
        p5 = Parada.objects.create(itinerario=self.itinerario, comercio=self.c1, orden=5, estado=EstadoParada.PENDIENTE)
        payload = {"nombre": "Ruta Multiparada", "parada_ids": [self.p1.id, self.p2.id, p5.id]}
        request = self.factory.post("/api/itinerarios/crear-ruta/", payload, format="json")
        force_authenticate(request, user=self.user)
        response = ItinerarioViewSet.as_view({"post": "crear_ruta"})(request)

        self.assertEqual(response.status_code, 201)
        ruta = RutaGuardada.objects.get(nombre="Ruta Multiparada")
        # Debe haber deduplicado c1 y contener exactamente 2 detalles (c1 y c2)
        detalles = list(ruta.detalles.all())
        self.assertEqual(len(detalles), 2)
        comercios_en_ruta = [d.comercio_id for d in detalles]
        self.assertEqual(set(comercios_en_ruta), {self.c1.id, self.c2.id})

    def test_crear_ruta_no_reordena_itinerario(self):
        # Verificar que guardar una plantilla no modifique el orden del itinerario activo
        # Paradas iniciales: p1(FINALIZADA,orden=1), p2(PENDIENTE,orden=2), p3(PENDIENTE,orden=3), p4(PENDIENTE,orden=4)
        ordenes_antes = {
            self.p1.id: 1,
            self.p2.id: 2,
            self.p3.id: 3,
            self.p4.id: 4,
        }

        # Guardar una plantilla con orden diferente: p4, p3, p1, p2
        payload = {
            "nombre": "Ruta Diferentes Orden",
            "parada_ids": [self.p4.id, self.p3.id, self.p1.id, self.p2.id],
        }
        request = self.factory.post("/api/itinerarios/crear-ruta/", payload, format="json")
        force_authenticate(request, user=self.user)
        response = ItinerarioViewSet.as_view({"post": "crear_ruta"})(request)

        self.assertEqual(response.status_code, 201)

        # Verificar que el orden del itinerario NO cambió
        self.p1.refresh_from_db()
        self.p2.refresh_from_db()
        self.p3.refresh_from_db()
        self.p4.refresh_from_db()

        self.assertEqual(self.p1.orden, ordenes_antes[self.p1.id])
        self.assertEqual(self.p2.orden, ordenes_antes[self.p2.id])
        self.assertEqual(self.p3.orden, ordenes_antes[self.p3.id])
        self.assertEqual(self.p4.orden, ordenes_antes[self.p4.id])

        # Verificar que la ruta SÍ fue creada con el orden correcto
        ruta = RutaGuardada.objects.get(nombre="Ruta Diferentes Orden")
        detalles = list(ruta.detalles.order_by("prioridad"))
        self.assertEqual(len(detalles), 4)
        self.assertEqual(detalles[0].comercio_id, self.c4.id)
        self.assertEqual(detalles[1].comercio_id, self.c3.id)
        self.assertEqual(detalles[2].comercio_id, self.c1.id)
        self.assertEqual(detalles[3].comercio_id, self.c2.id)

    def test_ordenar_por_ruta_preserva_slots_con_parada_finalizada_en_inicio(self):
        # p1 (FINALIZADA) en slot 1. Pendientes: p2 (slot 2), p3 (slot 3), p4 (slot 4)
        ruta = RutaGuardada.objects.create(transportista=self.transportista, nombre="Ruta Prioridad Inversa")
        DetalleRutaGuardada.objects.create(ruta_guardada=ruta, comercio=self.c4, prioridad=1)
        DetalleRutaGuardada.objects.create(ruta_guardada=ruta, comercio=self.c3, prioridad=2)
        DetalleRutaGuardada.objects.create(ruta_guardada=ruta, comercio=self.c2, prioridad=3)

        payload = {"ruta_id": ruta.id}
        request = self.factory.post("/api/itinerarios/ordenar-por-ruta/", payload, format="json")
        force_authenticate(request, user=self.user)
        response = ItinerarioViewSet.as_view({"post": "ordenar_por_ruta"})(request)

        self.assertEqual(response.status_code, 200)
        self.p1.refresh_from_db()
        self.p4.refresh_from_db()
        self.p3.refresh_from_db()
        self.p2.refresh_from_db()

        # p1 queda intacta en slot 1
        self.assertEqual(self.p1.orden, 1)
        # Las pendientes ocupan slots 2, 3, 4 según prioridad de plantilla
        self.assertEqual(self.p4.orden, 2)
        self.assertEqual(self.p3.orden, 3)
        self.assertEqual(self.p2.orden, 4)

    def test_ordenar_por_ruta_preserva_slots_con_parada_finalizada_intercalada(self):
        # Escenario crítico señalado por el equipo: cobro out-of-order
        # p3 (en slot 3) fue cobrada out-of-order y está FINALIZADA.
        # p1 (slot 1), p2 (slot 2) y p4 (slot 4) siguen PENDIENTES.
        self.p1.estado = EstadoParada.PENDIENTE
        self.p1.save()
        self.p3.estado = EstadoParada.FINALIZADA
        self.p3.save()

        # Plantilla prioriza: c4 (1), c2 (2), c1 (3)
        ruta = RutaGuardada.objects.create(transportista=self.transportista, nombre="Ruta Out-of-order")
        DetalleRutaGuardada.objects.create(ruta_guardada=ruta, comercio=self.c4, prioridad=1)
        DetalleRutaGuardada.objects.create(ruta_guardada=ruta, comercio=self.c2, prioridad=2)
        DetalleRutaGuardada.objects.create(ruta_guardada=ruta, comercio=self.c1, prioridad=3)

        payload = {"ruta_id": ruta.id}
        request = self.factory.post("/api/itinerarios/ordenar-por-ruta/", payload, format="json")
        force_authenticate(request, user=self.user)
        response = ItinerarioViewSet.as_view({"post": "ordenar_por_ruta"})(request)

        self.assertEqual(response.status_code, 200)
        self.p1.refresh_from_db()
        self.p2.refresh_from_db()
        self.p3.refresh_from_db()
        self.p4.refresh_from_db()

        # p3 (FINALIZADA) conserva inalterado su slot 3 (NO salta a 1 ni se renúmera)
        self.assertEqual(self.p3.orden, 3)
        # Las paradas pendientes se distribuyen ordenadas en los slots libres [1, 2, 4]:
        # c4 (prioridad 1) toma slot 1
        self.assertEqual(self.p4.orden, 1)
        # c2 (prioridad 2) toma slot 2
        self.assertEqual(self.p2.orden, 2)
        # c1 (prioridad 3) toma slot 4
        self.assertEqual(self.p1.orden, 4)



