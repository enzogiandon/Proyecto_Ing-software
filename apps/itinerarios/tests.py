from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from apps.core.models import Roles, Transportista, Vehiculo
from apps.remitos.models import Comercio, EstadoRemito, Marca, Remito

from .models import EstadoItinerario, Itinerario, Parada
from .services import crear_paradas


class ItinerarioViewsTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.administrativo = user_model.objects.create_user(
            username="planificador",
            password="Testing-Password-123!",
            dni="12345678",
            rol=Roles.ADMINISTRATIVO,
        )
        permissions = Permission.objects.filter(
            content_type__app_label__in=["itinerarios", "remitos"],
            codename__in=[
                "view_itinerario",
                "add_itinerario",
                "add_parada",
                "change_remito",
            ],
        )
        self.administrativo.user_permissions.add(*permissions)
        self.client.force_login(self.administrativo)

        self.vehiculo = Vehiculo.objects.create(patente="AB123CD")
        self.transportista_user = user_model.objects.create_user(
            username="transportista",
            password="Driver-Password-123!",
            dni="23456789",
            rol=Roles.TRANSPORTISTA,
        )
        self.transportista = Transportista.objects.create(
            usuario=self.transportista_user,
            vehiculo=self.vehiculo,
        )
        self.marca = Marca.objects.create(nombre="Marca", cuit="20123456789")

    def crear_comercio(self, razon_social, cuit):
        return Comercio.objects.create(
            razon_social=razon_social,
            cuit=cuit,
            domicilio=f"Dirección {razon_social}",
        )

    def crear_remito(self, comercio, numero):
        return Remito.objects.create(
            numero=numero,
            marca=self.marca,
            fecha_emision=date(2026, 10, 21),
            fecha_pactada=date(2026, 10, 22),
            comercio=comercio,
        )

    def test_create_itinerary_uses_transportista_vehicle(self):
        second_vehiculo = Vehiculo.objects.create(patente="CD456EF")
        second_user = get_user_model().objects.create_user(
            username="transportista2",
            password="Driver-Password-123!",
            dni="34567890",
            rol=Roles.TRANSPORTISTA,
        )
        second_transportista = Transportista.objects.create(
            usuario=second_user,
            vehiculo=second_vehiculo,
        )

        response = self.client.post(
            reverse("itinerarios:itinerario_crear"),
            {
                "fecha": "2026-10-25",
                "transportistas": [
                    self.transportista.pk,
                    second_transportista.pk,
                ],
            },
        )

        self.assertRedirects(
            response,
            reverse("itinerarios:itinerario_lista"),
            fetch_redirect_response=False,
        )
        self.assertEqual(Itinerario.objects.count(), 2)
        itinerario = Itinerario.objects.get(transportista=self.transportista)
        self.assertEqual(itinerario.vehiculo, self.vehiculo)
        self.assertEqual(itinerario.fecha, date(2026, 10, 25))
        self.assertEqual(itinerario.estado, EstadoItinerario.PENDIENTE)

    def test_create_stops_assigns_pending_receipts_to_existing_itinerary(self):
        itinerario = Itinerario.objects.create(
            fecha=date(2026, 10, 25),
            transportista=self.transportista,
            vehiculo=self.vehiculo,
        )
        comercio = self.crear_comercio("Comercio", "20123456789")
        remito_a = self.crear_remito(comercio, "R-001")
        remito_b = self.crear_remito(comercio, "R-002")

        response = self.client.post(
            reverse("itinerarios:paradas_crear"),
            {
                "itinerario": itinerario.pk,
                "comercios": [comercio.pk],
            },
        )

        self.assertRedirects(
            response,
            reverse("itinerarios:itinerario_lista"),
            fetch_redirect_response=False,
        )
        self.assertEqual(Parada.objects.filter(itinerario=itinerario).count(), 1)
        remito_a.refresh_from_db()
        remito_b.refresh_from_db()
        self.assertEqual(remito_a.estado, EstadoRemito.ASIGNADO)
        self.assertEqual(remito_b.estado, EstadoRemito.ASIGNADO)
        self.assertEqual(remito_a.parada, remito_b.parada)

    def test_create_stops_rejects_commerce_without_pending_receipts(self):
        itinerario = Itinerario.objects.create(
            fecha=date(2026, 10, 25),
            transportista=self.transportista,
            vehiculo=self.vehiculo,
        )
        comercio = self.crear_comercio("Comercio sin remitos", "20123456790")

        with self.assertRaisesMessage(
            ValidationError,
            f'El comercio "{comercio}" ya no tiene remitos pendientes.',
        ):
            crear_paradas(itinerario, [comercio])
        self.assertFalse(Parada.objects.filter(itinerario=itinerario).exists())
