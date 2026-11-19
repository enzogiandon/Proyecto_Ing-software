from datetime import date
from decimal import Decimal
import io
from PIL import Image

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.api.views import ParadaViewSet
from apps.cobranza.models import Cobranza
from apps.core.models import Transportista
from apps.itinerarios.models import EstadoItinerario, EstadoParada, Itinerario, Parada
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

    def test_subir_evidencia_rejects_non_image_files(self):
        text_file = SimpleUploadedFile(
            "nota.txt", b"este no es un archivo de imagen", content_type="text/plain"
        )
        request = self.factory.post(
            f"/api/paradas/{self.parada.id}/subir-evidencia/",
            {"archivo": text_file},
            format="multipart",
        )
        force_authenticate(request, user=self.user)

        response = ParadaViewSet.as_view({"post": "subir_evidencia"})(
            request,
            pk=self.parada.pk,
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("archivo", response.data)

    def test_subir_evidencia_accepts_valid_image(self):
        buffer = io.BytesIO()
        image = Image.new("RGB", (100, 100), color="blue")
        image.save(buffer, format="JPEG")
        image_file = SimpleUploadedFile(
            "foto.jpg", buffer.getvalue(), content_type="image/jpeg"
        )

        request = self.factory.post(
            f"/api/paradas/{self.parada.id}/subir-evidencia/",
            {"archivo": image_file},
            format="multipart",
        )
        force_authenticate(request, user=self.user)

        response = ParadaViewSet.as_view({"post": "subir_evidencia"})(
            request,
            pk=self.parada.pk,
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(self.parada.evidencias.exists())
