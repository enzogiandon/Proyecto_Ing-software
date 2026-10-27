from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from apps.core.models import Roles, Transportista, Vehiculo
from apps.itinerarios.models import (
    DetalleRutaGuardada,
    EstadoItinerario,
    EvidenciaParada,
    Itinerario,
    Parada,
    ProblemaParada,
)
from apps.itinerarios.services import crear_paradas
from apps.remitos.models import Comercio, EstadoRemito, Marca, Remito


class ItinerarioViewsTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.administrativo = user_model.objects.create_user(
            username="11111111",
            password="Testing-Password-123!",
            rol=Roles.ADMINISTRATIVO,
        )
        permissions = Permission.objects.filter(
            content_type__app_label__in=["itinerarios", "remitos"],
            codename__in=[
                "view_itinerario",
                "view_parada",
                "add_itinerario",
                "add_parada",
                "change_remito",
            ],
        )
        self.administrativo.user_permissions.add(*permissions)
        self.client.force_login(self.administrativo)

        self.vehiculo = Vehiculo.objects.create(patente="AB123CD")
        self.transportista_user = user_model.objects.create_user(
            username="22222222",
            password="Driver-Password-123!",
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
            comercio=comercio,
            total=0,
        )

    def test_create_itinerary_uses_transportista_vehicle(self):
        second_vehiculo = Vehiculo.objects.create(patente="CD456EF")
        second_user = get_user_model().objects.create_user(
            username="33333333",
            password="Driver-Password-123!",
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
        self.assertEqual(itinerario.estado, EstadoItinerario.ASIGNADO)

    def test_create_stops_assigns_pending_receipts_to_existing_itinerary(self):
        itinerario = Itinerario.objects.create(
            fecha=date(2026, 10, 25),
            transportista=self.transportista,
            vehiculo=self.vehiculo,
            estado=EstadoItinerario.ASIGNADO,
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
            estado=EstadoItinerario.ASIGNADO,
        )
        comercio = self.crear_comercio("Comercio sin remitos", "20123456790")

        with self.assertRaisesMessage(
            ValidationError,
            f'El comercio "{comercio}" ya no tiene remitos pendientes.',
        ):
            crear_paradas(itinerario, [comercio])
        self.assertFalse(Parada.objects.filter(itinerario=itinerario).exists())

    def test_delivery_detail_shows_receipts_evidence_and_contingencies(self):
        itinerario = Itinerario.objects.create(
            fecha=date(2026, 10, 25),
            transportista=self.transportista,
            vehiculo=self.vehiculo,
            estado=EstadoItinerario.ASIGNADO,
        )
        comercio = self.crear_comercio("Comercio detalle", "20123456790")
        parada = Parada.objects.create(
            itinerario=itinerario,
            comercio=comercio,
            orden=1,
        )
        remito_a = self.crear_remito(comercio, "R-DET-001")
        remito_b = self.crear_remito(comercio, "R-DET-002")
        remito_eliminado = self.crear_remito(comercio, "R-DET-003")
        remito_a.parada = parada
        remito_b.parada = parada
        remito_eliminado.parada = parada
        remito_a.save(update_fields=["parada"])
        remito_b.save(update_fields=["parada"])
        remito_eliminado.save(update_fields=["parada"])
        remito_eliminado.delete()
        EvidenciaParada.objects.create(
            parada=parada,
            archivo="remitos_firmados/evidencia.jpg",
        )
        ProblemaParada.objects.create(
            parada=parada,
            descripcion="Comercio cerrado",
            impide_entrega=True,
        )

        response = self.client.get(
            reverse("itinerarios:parada_detalle", args=[parada.pk])
        )
        list_response = self.client.get(reverse("itinerarios:itinerario_lista"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            list_response,
            reverse("itinerarios:parada_detalle", args=[parada.pk]),
        )
        self.assertContains(response, "Comercio detalle")
        self.assertContains(response, "Dirección Comercio detalle")
        self.assertContains(response, "R-DET-001")
        self.assertContains(response, "R-DET-002")
        self.assertNotContains(response, "R-DET-003")
        self.assertContains(response, "evidencia.jpg")
        self.assertContains(response, "Comercio cerrado")
        self.assertContains(
            response,
            reverse("remitos:remito_detalle", args=[remito_a.pk]),
        )

        remito_response = self.client.get(
            reverse("remitos:remito_detalle", args=[remito_a.pk])
        )
        self.assertEqual(remito_response.status_code, 200)
        self.assertContains(remito_response, "$0,00")

    def test_delivery_list_shows_error_stops_before_other_statuses(self):
        itinerario = Itinerario.objects.create(
            fecha=date(2026, 10, 25),
            transportista=self.transportista,
            vehiculo=self.vehiculo,
        )
        paradas = [
            Parada.objects.create(
                itinerario=itinerario,
                comercio=self.crear_comercio("Pendiente", "20123456790"),
                orden=1,
                estado="pendiente",
            ),
            Parada.objects.create(
                itinerario=itinerario,
                comercio=self.crear_comercio("Error", "20123456791"),
                orden=2,
                estado="error",
            ),
            Parada.objects.create(
                itinerario=itinerario,
                comercio=self.crear_comercio("Finalizada", "20123456792"),
                orden=3,
                estado="finalizada",
            ),
            Parada.objects.create(
                itinerario=itinerario,
                comercio=self.crear_comercio("Resuelto", "20123456793"),
                orden=4,
                estado="resuelto",
            ),
        ]

        response = self.client.get(reverse("itinerarios:itinerario_lista"))

        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        positions = [
            content.index(f">{parada.comercio.razon_social}<")
            for parada in [paradas[1], paradas[0], paradas[2], paradas[3]]
        ]
        self.assertEqual(positions, sorted(positions))


class ItinerariosModelTests(TestCase):
    def test_saved_route_details_keep_order_and_unique_commerce_constraint(self):
        self.assertEqual(
            DetalleRutaGuardada._meta.constraints[0].name,
            "unique_comercio",
        )
        self.assertEqual(
            DetalleRutaGuardada._meta.ordering[0].nulls_last,
            True,
        )

    def test_problem_string_uses_commerce_business_name(self):
        comercio = Comercio(razon_social="Comercio de prueba")
        parada = Parada(id=1, comercio=comercio)
        problema = ProblemaParada(parada=parada)

        self.assertEqual(
            str(problema),
            "Problema [Otro problema] - Parada #1 (Comercio de prueba)",
        )
