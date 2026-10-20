from datetime import date, timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from django.test import Client, TestCase
from django.urls import reverse

from apps.remitos.forms import (
    BaseItemRemitoFormSet,
    ImportacionRemitosForm,
    ItemRemitoForm,
    ItemRemitoFormSet,
    RemitoForm,
)
from apps.remitos.models import (
    Comercio,
    ErrorImportacion,
    EstadoImportacion,
    EstadoRemito,
    ImportacionRemitos,
    ItemRemito,
    Marca,
    Producto,
    Remito,
)


class BaseTestCase(TestCase):
    """Configuración base de entidades requeridas por las pruebas."""

    def setUp(self):
        self.client = Client()

        self.marca = Marca.objects.create(
            nombre="Marca Test",
            cuit="20123456789",
            contacto="Juan Perez",
            telefono="1122334455",
            email="contacto@marcatest.com",
        )

        self.comercio = Comercio.objects.create(
            razon_social="Comercio Central SRL",
            cuit="30987654321",
            domicilio="Av. Siempre Viva 742",
            telefono="1199887766",
        )

        self.producto_1 = Producto.objects.create(
            nombre="Producto A", codigo="PROD-001", marca=self.marca
        )
        self.producto_2 = Producto.objects.create(
            nombre="Producto B", codigo="PROD-002", marca=self.marca
        )


# ==============================================================================
# 1. TESTS DE MODELOS
# ==============================================================================
class ModelosRemitosTests(BaseTestCase):
    def test_str_modelos(self):
        self.assertEqual(str(self.marca), "Marca Test")
        self.assertIn("Comercio Central SRL", str(self.comercio))
        self.assertEqual(str(self.producto_1), "Producto A - PROD-001")

    def test_cuit_comercio_invalido_falla(self):
        comercio_invalido = Comercio(
            razon_social="Invalido SA", cuit="12345", domicilio="Calle Falsa 123"
        )
        with self.assertRaises(ValidationError):
            comercio_invalido.full_clean()

    def test_creacion_remito_e_items(self):
        remito = Remito.objects.create(
            numero="R-0001",
            marca=self.marca,
            monto_total=Decimal("1500.50"),
            estado=EstadoRemito.PENDIENTE,
            fecha_emision=date.today(),
            fecha_pactada=date.today() + timedelta(days=2),
            comercio=self.comercio,
        )
        item = ItemRemito.objects.create(
            remito=remito,
            producto=self.producto_1,
            cantidad=3,
            precio_unitario=Decimal("500.00"),
        )
        self.assertEqual(remito.items.count(), 1)
        self.assertEqual(item.cantidad, 3)
        self.assertEqual(str(remito), "Remito #R-0001 - Comercio Central SRL")

    def test_ruta_archivo_importacion(self):
        archivo_mock = SimpleUploadedFile(
            "planilla.csv", b"col1,col2\n1,2", content_type="text/csv"
        )
        importacion = ImportacionRemitos.objects.create(
            archivo=archivo_mock,
            marca=self.marca,
            estado=EstadoImportacion.RECHAZADO,
        )
        self.assertTrue(importacion.archivo.name.startswith("importaciones/lote_"))
        self.assertTrue(importacion.archivo.name.endswith(".csv"))


    def test_modelo_remito_numero_duplicado_lanza_integrity_error(self):
        Remito.objects.create(
            numero="R-UNICO",
            marca=self.marca,
            monto_total=Decimal("500.00"),
            fecha_emision=date.today(),
            fecha_pactada=date.today(),
            comercio=self.comercio,
        )

        # Al intentar guardar otro con el mismo número, la base de datos debe frenarlo
        with self.assertRaises(IntegrityError):
            Remito.objects.create(
                numero="R-UNICO",
                marca=self.marca,
                monto_total=Decimal("700.00"),
                fecha_emision=date.today(),
                fecha_pactada=date.today(),
                comercio=self.comercio,
            )


# ==============================================================================
# 2. TESTS DE FORMS Y FORMSETS
# ==============================================================================
class FormulariosRemitosTests(BaseTestCase):
    def test_remito_form_fecha_pactada_anterior_a_hoy_invalida(self):
        data = {
            "numero": "REM-100",
            "marca": self.marca.id,
            "monto_total": "250.00",
            "fecha_emision": date.today(),
            "fecha_pactada": date.today() - timedelta(days=1),  # Fecha pasada
            "comercio": self.comercio.id,
        }
        form = RemitoForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("fecha_pactada", form.errors)

    def test_remito_form_valido(self):
        data = {
            "numero": "REM-101",
            "marca": self.marca.id,
            "monto_total": "250.00",
            "fecha_emision": date.today(),
            "fecha_pactada": date.today() + timedelta(days=3),
            "comercio": self.comercio.id,
        }
        form = RemitoForm(data=data)
        self.assertTrue(form.is_valid())

    def test_item_remito_form_precio_unitario_cero_o_negativo(self):
        form_cero = ItemRemitoForm(
            data={
                "producto": self.producto_1.id,
                "cantidad": 1,
                "precio_unitario": "0.00",
            }
        )
        self.assertFalse(form_cero.is_valid())
        self.assertIn("precio_unitario", form_cero.errors)

        form_negativo = ItemRemitoForm(
            data={
                "producto": self.producto_1.id,
                "cantidad": 1,
                "precio_unitario": "-15.00",
            }
        )
        self.assertFalse(form_negativo.is_valid())
        self.assertIn("precio_unitario", form_negativo.errors)

    def test_formset_detecta_productos_duplicados(self):
        data = {
            "items-TOTAL_FORMS": "2",
            "items-INITIAL_FORMS": "0",
            "items-MIN_NUM_FORMS": "0",
            "items-MAX_NUM_FORMS": "1000",
            # Fila 1
            "items-0-producto": self.producto_1.id,
            "items-0-cantidad": "2",
            "items-0-precio_unitario": "100.00",
            # Fila 2 (mismo producto)
            "items-1-producto": self.producto_1.id,
            "items-1-cantidad": "5",
            "items-1-precio_unitario": "100.00",
        }
        formset = ItemRemitoFormSet(data=data, prefix="items")
        self.assertFalse(formset.is_valid())
        self.assertTrue(
            any(
                f'El producto "{self.producto_1.nombre}" está repetido' in err
                for err in formset.non_form_errors()
            )
        )


    def test_remito_form_numero_duplicado_invalido(self):
        # 1. Creamos un remito existente
        Remito.objects.create(
            numero="R-DUPLICADO",
            marca=self.marca,
            monto_total=Decimal("1000.00"),
            estado=EstadoRemito.PENDIENTE,
            fecha_emision=date.today(),
            fecha_pactada=date.today() + timedelta(days=1),
            comercio=self.comercio,
        )

        # 2. Intentamos validar un formulario con el número
        data = {
            "numero": "R-DUPLICADO",
            "marca": self.marca.id,
            "monto_total": "500.00",
            "fecha_emision": date.today(),
            "fecha_pactada": date.today() + timedelta(days=2),
            "comercio": self.comercio.id,
        }
        form = RemitoForm(data=data)

        # Debe fallar la validación y marcar error en 'numero'
        self.assertFalse(form.is_valid())
        self.assertIn("numero", form.errors)




# ==============================================================================
# 3. TESTS DE VISTAS (CBVs)
# ==============================================================================
class VistasRemitosTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.remito = Remito.objects.create(
            numero="R-5555",
            marca=self.marca,
            monto_total=Decimal("800.00"),
            estado=EstadoRemito.PENDIENTE,
            fecha_emision=date.today(),
            fecha_pactada=date.today(),
            comercio=self.comercio,
        )

    def test_lista_remitos_status_y_contexto(self):
        response = self.client.get(reverse("remitos:remito_lista"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("remitos", response.context)
        self.assertEqual(len(response.context["remitos"]), 1)

    def test_detalle_remito_view(self):
        response = self.client.get(
            reverse("remitos:remito_detalle", kwargs={"pk": self.remito.pk})
        )
        self.assertEqual(response.status_code, 200)
        # Requiere haber corregido context_object_name en DetalleRemito
        self.assertEqual(response.context["remito"], self.remito)

    def test_crear_remito_con_items_exitoso(self):
        post_data = {
            # Campos del RemitoForm
            "numero": "R-9999",
            "marca": self.marca.id,
            "monto_total": "1200.00",
            "fecha_emision": str(date.today()),
            "fecha_pactada": str(date.today() + timedelta(days=1)),
            "comercio": self.comercio.id,
            # Gestión del FormSet de Items
            "items-TOTAL_FORMS": "2",
            "items-INITIAL_FORMS": "0",
            "items-MIN_NUM_FORMS": "0",
            "items-MAX_NUM_FORMS": "1000",
            "items-0-producto": self.producto_1.id,
            "items-0-cantidad": "2",
            "items-0-precio_unitario": "300.00",
            "items-1-producto": self.producto_2.id,
            "items-1-cantidad": "1",
            "items-1-precio_unitario": "600.00",
        }
        response = self.client.post(reverse("remitos:remito_crear"), data=post_data)

        self.assertEqual(response.status_code, 302)  # Redirección de éxito
        nuevo_remito = Remito.objects.get(numero="R-9999")
        self.assertEqual(nuevo_remito.items.count(), 2)

    def test_editar_remito_view(self):
        # Requiere haber corregido items_formset.instance en EditarRemito.form_valid
        post_data = {
            "numero": self.remito.numero,
            "marca": self.marca.id,
            "monto_total": "999.00",  # Actualizamos monto
            "fecha_emision": str(self.remito.fecha_emision),
            "fecha_pactada": str(self.remito.fecha_pactada),
            "comercio": self.comercio.id,
            "items-TOTAL_FORMS": "0",
            "items-INITIAL_FORMS": "0",
            "items-MIN_NUM_FORMS": "0",
            "items-MAX_NUM_FORMS": "1000",
        }
        response = self.client.post(
            reverse("remitos:remito_editar", kwargs={"pk": self.remito.pk}),
            data=post_data,
        )
        self.assertEqual(response.status_code, 302)
        self.remito.refresh_from_db()
        self.assertEqual(self.remito.monto_total, Decimal("999.00"))

    def test_subir_archivo_importacion_create_view(self):
        archivo_fake = SimpleUploadedFile(
            "lote_test.csv",
            b"remito,monto\n1001,500.00",
            content_type="text/csv",
        )
        post_data = {"marca": self.marca.id, "archivo": archivo_fake}
        response = self.client.post(
            reverse("remitos:importacion_crear"), data=post_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(ImportacionRemitos.objects.count(), 1)


    def test_crear_remito_post_con_numero_duplicado_no_crea_registro(self):
        # Remito previo
        Remito.objects.create(
            numero="R-EXISTENTE",
            marca=self.marca,
            monto_total=Decimal("1000.00"),
            estado=EstadoRemito.PENDIENTE,
            fecha_emision=date.today(),
            fecha_pactada=date.today(),
            comercio=self.comercio,
        )

        post_data = {
            "numero": "R-EXISTENTE",  # Mismo número
            "marca": self.marca.id,
            "monto_total": "2000.00",
            "fecha_emision": str(date.today()),
            "fecha_pactada": str(date.today() + timedelta(days=1)),
            "comercio": self.comercio.id,
            "items-TOTAL_FORMS": "0",
            "items-INITIAL_FORMS": "0",
            "items-MIN_NUM_FORMS": "0",
            "items-MAX_NUM_FORMS": "1000",
        }

        response = self.client.post(reverse("remitos:remito_crear"), data=post_data)

        self.assertEqual(response.status_code, 200)

        form = response.context["form"]
        self.assertFalse(form.is_valid())
        self.assertIn("numero", form.errors)

        self.assertEqual(Remito.objects.filter(numero="R-EXISTENTE").count(), 1)


    def test_crear_remito_falla_en_items_cancela_creacion_remito(self):
        """Si los items son inválidos, el bloque transaction.atomic debe hacer rollback."""
        post_data = {
            "numero": "R-ROLLBACK",
            "marca": self.marca.id,
            "monto_total": "1000.00",
            "fecha_emision": str(date.today()),
            "fecha_pactada": str(date.today() + timedelta(days=1)),
            "comercio": self.comercio.id,
            # Formset con error (precio negativo)
            "items-TOTAL_FORMS": "1",
            "items-INITIAL_FORMS": "0",
            "items-MIN_NUM_FORMS": "0",
            "items-MAX_NUM_FORMS": "1000",
            "items-0-producto": self.producto_1.id,
            "items-0-cantidad": "2",
            "items-0-precio_unitario": "-50.00",  # Inválido
        }

        response = self.client.post(reverse("remitos:remito_crear"), data=post_data)

        self.assertEqual(response.status_code, 200)
        # Verificamos que gracias a la validación / atomicidad, el remito NO exista en DB
        self.assertFalse(Remito.objects.filter(numero="R-ROLLBACK").exists())
