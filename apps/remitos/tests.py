from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from apps.remitos.forms import RemitoForm
from apps.remitos.models import Comercio, EstadoRemito, Marca, Remito


class RemitoTestCase(TestCase):
    def setUp(self):
        self.comercio = Comercio.objects.create(
            razon_social="Comercio de prueba",
            cuit="30112233445",
            domicilio="Av. Principal 123",
        )
        self.marca = Marca.objects.create(
            nombre="Marca de prueba",
            cuit="30998877665",
        )

    def datos_remito(self, **overrides):
        data = {
            "numero": "R-001",
            "marca": self.marca.pk,
            "comercio": self.comercio.pk,
            "total": "1250.50",
        }
        data.update(overrides)
        return data


class RemitoModelTests(RemitoTestCase):
    def test_delete_is_soft_delete(self):
        remito = Remito.objects.create(
            numero="R-001",
            marca=self.marca,
            comercio=self.comercio,
            total=Decimal("1250.50"),
        )

        remito.delete()

        remito.refresh_from_db()
        self.assertTrue(remito.eliminado)
        self.assertTrue(Remito.objects.filter(pk=remito.pk).exists())

    def test_string_representation_contains_number_and_commerce(self):
        remito = Remito.objects.create(
            numero="R-002",
            marca=self.marca,
            comercio=self.comercio,
            total=Decimal("1250.50"),
        )

        self.assertEqual(str(remito), "Remito #R-002 - Comercio de prueba")


class RemitoFormTests(RemitoTestCase):
    def test_form_accepts_current_remito_fields(self):
        form = RemitoForm(data=self.datos_remito())

        self.assertTrue(form.is_valid(), form.errors)

    def test_form_rejects_non_positive_total(self):
        form = RemitoForm(data=self.datos_remito(total="0.00"))

        self.assertFalse(form.is_valid())
        self.assertIn("El monto total tiene que ser mayor a cero.", form.errors["total"])


class RemitoViewsTests(RemitoTestCase):
    def test_create_remito_persists_data_and_redirects(self):
        response = self.client.post(
            reverse("remitos:remito_crear"),
            self.datos_remito(),
        )

        self.assertRedirects(
            response,
            reverse("remitos:remito_lista"),
            fetch_redirect_response=False,
        )
        remito = Remito.objects.get(numero="R-001")
        self.assertEqual(remito.total, Decimal("1250.50"))
        self.assertEqual(remito.estado, EstadoRemito.PENDIENTE)

    def test_create_remito_rejects_non_positive_total(self):
        response = self.client.post(
            reverse("remitos:remito_crear"),
            self.datos_remito(total="0.00"),
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Remito.objects.filter(numero="R-001").exists())
        self.assertContains(response, "El monto total tiene que ser mayor a cero.")

    def test_edit_remito_updates_fields_and_redirects(self):
        remito = Remito.objects.create(
            numero="R-003",
            marca=self.marca,
            comercio=self.comercio,
            total=Decimal("1250.50"),
        )

        response = self.client.post(
            reverse("remitos:remito_editar", args=[remito.pk]),
            self.datos_remito(numero="R-003", total="2400.00"),
        )

        self.assertRedirects(
            response,
            reverse("remitos:remito_lista"),
            fetch_redirect_response=False,
        )
        remito.refresh_from_db()
        self.assertEqual(remito.total, Decimal("2400.00"))

    def test_delete_remito_marks_it_deleted_and_redirects(self):
        remito = Remito.objects.create(
            numero="R-004",
            marca=self.marca,
            comercio=self.comercio,
            total=Decimal("1250.50"),
        )

        response = self.client.post(
            reverse("remitos:remito_eliminar", args=[remito.pk])
        )

        self.assertRedirects(
            response,
            reverse("remitos:remito_lista"),
            fetch_redirect_response=False,
        )
        remito.refresh_from_db()
        self.assertTrue(remito.eliminado)

    def test_remito_list_can_filter_by_commerce_and_status(self):
        matching = Remito.objects.create(
            numero="R-005",
            marca=self.marca,
            comercio=self.comercio,
            total=Decimal("1250.50"),
            estado=EstadoRemito.PENDIENTE,
        )
        other_comercio = Comercio.objects.create(
            razon_social="Otro comercio",
            cuit="30112233446",
            domicilio="Otra dirección",
        )
        Remito.objects.create(
            numero="R-006",
            marca=self.marca,
            comercio=other_comercio,
            total=Decimal("950.00"),
            estado=EstadoRemito.ENTREGADO,
        )

        response = self.client.get(
            reverse("remitos:remito_lista"),
            {"comercio": "Comercio de prueba", "estado": EstadoRemito.PENDIENTE},
        )

        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["remitos"],
            [matching],
        )
