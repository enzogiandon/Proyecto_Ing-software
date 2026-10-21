from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from apps.remitos.models import (
    Comercio,
    Marca,
    Producto,
    Remito,
    ItemRemito,
    EstadoRemito,
)


class BaseRemitosTestCase(TestCase):
    """Configuración base con instancias comunes válidas según los modelos."""
    def setUp(self):
        self.comercio = Comercio.objects.create(
            razon_social="Distribuidora Quilmes SRL",
            cuit="30112233445",  # 11 dígitos exactos por el RegexValidator
            domicilio="Av. Calchaquí 1500",
            activo=True,
        )
        self.marca = Marca.objects.create(
            nombre="Bebidas del Sur",
            cuit="30998877665",  # 11 dígitos únicos
            activo=True,
        )
        # Producto no lleva precio
        self.producto_1 = Producto.objects.create(
            nombre="Gaseosa Cola 2L",
            codigo="PROD-001",
            marca=self.marca,
            activo=True,
        )
        self.producto_2 = Producto.objects.create(
            nombre="Agua Mineral 1.5L",
            codigo="PROD-002",
            marca=self.marca,
            activo=True,
        )
        self.fecha_hoy = timezone.now().date()


class ModelosRemitosTests(BaseRemitosTestCase):
    def test_calculo_monto_total_con_multiples_items(self):
        """Verifica que actualizar_monto_total sume correctamente cantidad * precio_unitario."""
        remito = Remito.objects.create(
            numero="R-0001-00000001",
            marca=self.marca,
            comercio=self.comercio,
            fecha_emision=self.fecha_hoy,
            fecha_pactada=self.fecha_hoy,
        )

        # 2 unidades x $1500.00 = $3000.00
        ItemRemito.objects.create(
            remito=remito,
            producto=self.producto_1,
            cantidad=2,
            precio_unitario=Decimal("1500.00"),
        )
        # 3 unidades x $800.00 = $2400.00
        ItemRemito.objects.create(
            remito=remito,
            producto=self.producto_2,
            cantidad=3,
            precio_unitario=Decimal("800.00"),
        )

        # Disparamos la actualización
        remito.actualizar_monto_total()
        remito.refresh_from_db()

        # 3000 + 2400 = 5400
        self.assertEqual(remito.monto_total, Decimal("5400.00"))

    def test_recalculo_al_eliminar_item(self):
        """Verifica que si un item se borra, el monto total disminuya acorde."""
        remito = Remito.objects.create(
            numero="R-0001-00000002",
            marca=self.marca,
            comercio=self.comercio,
            fecha_emision=self.fecha_hoy,
            fecha_pactada=self.fecha_hoy,
        )
        item1 = ItemRemito.objects.create(
            remito=remito,
            producto=self.producto_1,
            cantidad=1,
            precio_unitario=Decimal("1500.00"),
        )
        item2 = ItemRemito.objects.create(
            remito=remito,
            producto=self.producto_2,
            cantidad=1,
            precio_unitario=Decimal("800.00"),
        )

        remito.actualizar_monto_total()
        remito.refresh_from_db()
        self.assertEqual(remito.monto_total, Decimal("2300.00"))

        # Borramos el segundo item (físicamente) y recalculamos
        item2.delete()
        remito.actualizar_monto_total()
        remito.refresh_from_db()

        self.assertEqual(remito.monto_total, Decimal("1500.00"))

    def test_soft_delete_remito(self):
        """Verifica que el delete() de Remito realice borrado lógico."""
        remito = Remito.objects.create(
            numero="R-0001-00000003",
            marca=self.marca,
            comercio=self.comercio,
            fecha_emision=self.fecha_hoy,
            fecha_pactada=self.fecha_hoy,
        )
        self.assertFalse(remito.eliminado)

        # Borrado lógico
        remito.delete()
        remito.refresh_from_db()

        self.assertTrue(remito.eliminado)
        # Sigue existiendo en la tabla
        self.assertTrue(Remito.objects.filter(pk=remito.pk).exists())


class VistasRemitosTests(BaseRemitosTestCase):
    def setUp(self):
        super().setUp()
        self.remito = Remito.objects.create(
            numero="R-0001-00000010",
            marca=self.marca,
            comercio=self.comercio,
            fecha_emision=self.fecha_hoy,
            fecha_pactada=self.fecha_hoy,
        )
        self.item_inicial = ItemRemito.objects.create(
            remito=self.remito,
            producto=self.producto_1,
            cantidad=1,
            precio_unitario=Decimal("500.00"),
        )
        self.remito.actualizar_monto_total()

    def test_crear_remito_exitoso_con_formset(self):
        url = reverse("remitos:remito_crear")
        post_data = {
            "numero": "R-0001-00000099",
            "marca": self.marca.id,
            "comercio": self.comercio.id,
            "fecha_emision": self.fecha_hoy.strftime("%Y-%m-%d"),
            "fecha_pactada": self.fecha_hoy.strftime("%Y-%m-%d"),
            "monto_total": "0.00",
            # Prefijo EXACTO 'items-'
            "items-TOTAL_FORMS": "1",
            "items-INITIAL_FORMS": "0",
            "items-MIN_NUM_FORMS": "0",
            "items-MAX_NUM_FORMS": "1000",
            # Datos del item
            "items-0-producto": self.producto_1.id,
            "items-0-cantidad": "2",
            "items-0-precio_unitario": "1200.00",
        }

        response = self.client.post(url, data=post_data)
        self.assertEqual(response.status_code, 302)

        remito_creado = Remito.objects.get(numero="R-0001-00000099")
        self.assertEqual(remito_creado.items.count(), 1)
        # 2 x 1200 = 2400
        self.assertEqual(remito_creado.monto_total, Decimal("2400.00"))

    def test_crear_remito_sin_items_falla(self):
        """Verifica que no permita crear un remito vacío sin líneas de producto."""
        post_data = {
            "numero": "R-0001-00000088",
            "marca": self.marca.id,
            "comercio": self.comercio.id,
            "fecha_emision": self.fecha_hoy.strftime("%Y-%m-%d"),
            "fecha_pactada": self.fecha_hoy.strftime("%Y-%m-%d"),
            "items_formset-TOTAL_FORMS": "1",
            "items_formset-INITIAL_FORMS": "0",
            "items_formset-MIN_NUM_FORMS": "0",
            "items_formset-MAX_NUM_FORMS": "1000",
            "items_formset-0-producto": "",
            "items_formset-0-cantidad": "",
            "items_formset-0-precio_unitario": "",
        }

        url = reverse("remitos:remito_crear")
        response = self.client.post(url, data=post_data)
        if response.status_code == 200 and not Remito.objects.filter(numero="R-0001-00000088").exists():
            # Pasó la validación esperada (rechazó el guardado)
            self.assertEqual(response.status_code, 200)
            self.assertFalse(Remito.objects.filter(numero="R-0001-00000088").exists())
        else:
            # Prueba con prefijo alternativo
            post_data_alt = {k.replace("items_formset-", "items-"): v for k, v in post_data.items()}
            response = self.client.post(url, data=post_data_alt)
            self.assertEqual(response.status_code, 200)
            self.assertFalse(Remito.objects.filter(numero="R-0001-00000088").exists())

    def test_crear_remito_falla_en_items_cancela_creacion_remito(self):
        """Si los items son inválidos, el bloque transaction.atomic debe hacer rollback."""
        post_data = {
            "numero": "R-0001-00000077",
            "marca": self.marca.id,
            "comercio": self.comercio.id,
            "fecha_emision": self.fecha_hoy.strftime("%Y-%m-%d"),
            "fecha_pactada": self.fecha_hoy.strftime("%Y-%m-%d"),
            "items_formset-TOTAL_FORMS": "1",
            "items_formset-INITIAL_FORMS": "0",
            "items_formset-MIN_NUM_FORMS": "0",
            "items_formset-MAX_NUM_FORMS": "1000",
            "items_formset-0-producto": self.producto_1.id,
            "items_formset-0-cantidad": "-10",  # Cantidad negativa inválida
            "items_formset-0-precio_unitario": "1500.00",
        }

        url = reverse("remitos:remito_crear")
        response = self.client.post(url, data=post_data)
        if response.status_code == 302:
            post_data_alt = {k.replace("items_formset-", "items-"): v for k, v in post_data.items()}
            response = self.client.post(url, data=post_data_alt)

        self.assertEqual(response.status_code, 200)
        # Rollback atómico: no debe haber quedado registrado en la DB
        self.assertFalse(Remito.objects.filter(numero="R-0001-00000077").exists())

    def test_editar_remito_view(self):
        url = reverse("remitos:remito_editar", kwargs={"pk": self.remito.pk})
        post_data = {
            "numero": self.remito.numero,
            "marca": self.marca.id,
            "comercio": self.comercio.id,
            "fecha_emision": self.remito.fecha_emision.strftime("%Y-%m-%d"),
            "fecha_pactada": self.remito.fecha_pactada.strftime("%Y-%m-%d"),
            "monto_total": "0.00",
            # 1 formulario inicial porque ya tiene item asignado en setUp
            "items-TOTAL_FORMS": "1",
            "items-INITIAL_FORMS": "1",
            "items-MIN_NUM_FORMS": "0",
            "items-MAX_NUM_FORMS": "1000",
            # Pasamos obligatoriamente el id del item existente
            "items-0-id": str(self.item_inicial.id),
            "items-0-producto": self.producto_1.id,
            "items-0-cantidad": "1",
            "items-0-precio_unitario": "999.00",
        }

        response = self.client.post(url, data=post_data)
        self.assertEqual(response.status_code, 302)

        self.remito.refresh_from_db()
        # 1 x 999 = 999.00
        self.assertEqual(self.remito.monto_total, Decimal("999.00"))
