import re
from decimal import Decimal
from io import StringIO

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from apps.core.models import Grupos
from apps.itinerarios.models import EstadoItinerario, EstadoParada, Itinerario, Parada
from apps.remitos.forms import RemitoForm
from apps.remitos.models import (
    Comercio,
    ErrorImportacion,
    EstadoImportacion,
    EstadoRemito,
    ImportacionRemitos,
    Marca,
    Remito,
    ruta_lote,
)


class RemitoTestCase(TestCase):
    def setUp(self):
        call_command("crear_grupos", stdout=StringIO())
        self.grupo_planificacion = Group.objects.get(
            name=Grupos.ADMIN_PLANIFICACION
        )
        user_model = get_user_model()
        self.usuario = user_model.objects.create_user(
            username="33333333",
            password="Test-Password-123!",
        )
        self.usuario.groups.add(self.grupo_planificacion)
        self.client.force_login(self.usuario)

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
    def test_delete_is_hard_delete(self):
        remito = Remito.objects.create(
            numero="R-001",
            marca=self.marca,
            comercio=self.comercio,
            total=Decimal("1250.50"),
        )
        pk = remito.pk
        remito.delete()

        self.assertFalse(Remito.objects.filter(pk=pk).exists())

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

    def test_form_rejects_modifying_numero_on_existing_remito(self):
        remito = Remito.objects.create(
            numero="R-001",
            marca=self.marca,
            comercio=self.comercio,
            total=Decimal("1250.50"),
        )
        form = RemitoForm(
            data=self.datos_remito(numero="R-MODIFICADO"),
            instance=remito,
        )

        self.assertFalse(form.is_valid())
        self.assertIn(
            "No está permitido modificar el número de remito una vez creado.",
            form.errors["numero"],
        )

    def test_form_allows_same_numero_on_existing_remito(self):
        remito = Remito.objects.create(
            numero="R-001",
            marca=self.marca,
            comercio=self.comercio,
            total=Decimal("1250.50"),
        )
        form = RemitoForm(
            data=self.datos_remito(numero="R-001", total="1500.00"),
            instance=remito,
        )

        self.assertTrue(form.is_valid(), form.errors)


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
        self.assertIsNone(remito.parada)

    def test_create_remito_assigns_existing_pending_stop_automatically(self):
        itinerario = Itinerario.objects.create(
            fecha="2026-11-15",
            estado=EstadoItinerario.ASIGNADO,
        )
        parada = Parada.objects.create(
            itinerario=itinerario,
            comercio=self.comercio,
            orden=1,
            estado=EstadoParada.PENDIENTE,
        )

        response = self.client.post(
            reverse("remitos:remito_crear"),
            self.datos_remito(numero="R-AUTO-1"),
        )

        self.assertRedirects(
            response,
            reverse("remitos:remito_lista"),
            fetch_redirect_response=False,
        )
        remito = Remito.objects.get(numero="R-AUTO-1")
        self.assertEqual(remito.parada, parada)
        self.assertEqual(remito.estado, EstadoRemito.ASIGNADO)

    def test_create_remito_ignores_non_pending_stops(self):
        itinerario = Itinerario.objects.create(
            fecha="2026-11-15",
            estado=EstadoItinerario.ASIGNADO,
        )
        Parada.objects.create(
            itinerario=itinerario,
            comercio=self.comercio,
            orden=1,
            estado=EstadoParada.FINALIZADA,
        )
        Parada.objects.create(
            itinerario=itinerario,
            comercio=self.comercio,
            orden=2,
            estado=EstadoParada.ERROR,
        )
        Parada.objects.create(
            itinerario=itinerario,
            comercio=self.comercio,
            orden=3,
            estado=EstadoParada.RESUELTO,
        )

        response = self.client.post(
            reverse("remitos:remito_crear"),
            self.datos_remito(numero="R-AUTO-2"),
        )

        self.assertRedirects(
            response,
            reverse("remitos:remito_lista"),
            fetch_redirect_response=False,
        )
        remito = Remito.objects.get(numero="R-AUTO-2")
        self.assertIsNone(remito.parada)
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
            reverse("remitos:remito_detalle", args=[remito.pk]),
            fetch_redirect_response=False,
        )
        remito.refresh_from_db()
        self.assertEqual(remito.total, Decimal("2400.00"))

    def test_edit_remito_rejects_modifying_numero(self):
        remito = Remito.objects.create(
            numero="R-003",
            marca=self.marca,
            comercio=self.comercio,
            total=Decimal("1250.50"),
        )

        response = self.client.post(
            reverse("remitos:remito_editar", args=[remito.pk]),
            self.datos_remito(numero="R-MODIFICADO", total="2400.00"),
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "No está permitido modificar el número de remito una vez creado.",
        )
        remito.refresh_from_db()
        self.assertEqual(remito.numero, "R-003")

    def test_edit_remito_only_allowed_in_pending_state(self):
        remito = Remito.objects.create(
            numero="R-003",
            marca=self.marca,
            comercio=self.comercio,
            total=Decimal("1250.50"),
            estado=EstadoRemito.ASIGNADO,
        )

        response = self.client.get(
            reverse("remitos:remito_editar", args=[remito.pk])
        )

        self.assertRedirects(
            response,
            reverse("remitos:remito_detalle", args=[remito.pk]),
            fetch_redirect_response=False,
        )

    def test_delete_remito_marks_it_deleted_and_redirects(self):
        itinerario = Itinerario.objects.create(
            fecha="2026-11-15",
            estado=EstadoItinerario.ASIGNADO,
        )
        parada = Parada.objects.create(
            itinerario=itinerario,
            comercio=self.comercio,
            orden=1,
            estado=EstadoParada.PENDIENTE,
        )
        remito = Remito.objects.create(
            numero="R-004",
            marca=self.marca,
            comercio=self.comercio,
            total=Decimal("1250.50"),
            parada=parada,
            estado=EstadoRemito.ASIGNADO,
        )

        response = self.client.post(
            reverse("remitos:remito_eliminar", args=[remito.pk])
        )

        self.assertRedirects(
            response,
            reverse("remitos:remito_lista"),
            fetch_redirect_response=False,
        )
        self.assertFalse(Remito.objects.filter(pk=remito.pk).exists())
        # La parada se quedó sin remitos activos, debe haberse eliminado
        self.assertFalse(Parada.objects.filter(pk=parada.pk).exists())

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


class ImportacionRemitosTestCase(TestCase):
    def setUp(self):
        call_command("crear_grupos", stdout=StringIO())
        self.grupo_planificacion = Group.objects.get(
            name=Grupos.ADMIN_PLANIFICACION
        )
        user_model = get_user_model()
        self.usuario = user_model.objects.create_user(
            username="44444444",
            password="Test-Password-123!",
        )
        self.usuario.groups.add(self.grupo_planificacion)
        self.client.force_login(self.usuario)

        self.marca1 = Marca.objects.create(
            nombre="Marca Uno",
            cuit="30654321090",
        )
        self.marca2 = Marca.objects.create(
            nombre="Marca Dos",
            cuit="30709876542",
        )

    def test_ruta_lote_maintains_filename_and_appends_hash(self):
        filename = "30654321090_20261027_DISTR-01.csv"
        path = ruta_lote(None, filename)
        # Debe guardarse en importaciones/
        self.assertTrue(path.startswith("importaciones/"))
        basename = path.replace("importaciones/", "")
        # Debe terminar en .csv y tener el nombre original + guion bajo + hash
        pattern = r"^30654321090_20261027_DISTR-01_[a-f0-9]{8}\.csv$"
        self.assertRegex(basename, pattern)

    def test_importar_remitos_multiple_archivos_con_cuit_en_nombre(self):
        csv_content1 = (
            "cuit_comercio,condicion_iva,numero_iibb,razon_social,domicilio,monto_a_cobrar,fecha_factura,numero_sucursal,numero_factura\n"
            "20301112223,Monotributo,976-123456-1,Kiosco Central,\"Calle 1 123\",15000.50,2026-10-21,0001,00001001\n"
            "20301112224,Exento,976-123456-2,Almacen Sur,\"Calle 2 456\",25000.00,2026-10-21,0001,00001002\n"
        ).encode("utf-8")
        csv_content2 = (
            "cuit_comercio,condicion_iva,numero_iibb,razon_social,domicilio,monto_a_cobrar,fecha_factura,numero_sucursal,numero_factura\n"
            "20301112225,Monotributo,976-123456-3,Maxikiosco Norte,\"Calle 3 789\",35000.75,2026-10-21,0002,00002001\n"
        ).encode("utf-8")

        file1 = SimpleUploadedFile("30654321090_20261027_DISTR-01.csv", csv_content1)
        file2 = SimpleUploadedFile("30709876542_20261027_DISTR-02.csv", csv_content2)

        response = self.client.post(
            reverse("remitos:importacion_crear"),
            {
                "archivo": [file1, file2],
            },
        )
        self.assertRedirects(response, reverse("core:inicio"), fetch_redirect_response=False)

        importaciones = ImportacionRemitos.objects.all().order_by("id")
        self.assertEqual(importaciones.count(), 2)

        imp1 = importaciones[0]
        self.assertEqual(imp1.marca, self.marca1)
        self.assertEqual(imp1.cantidad, 2)
        self.assertEqual(imp1.estado, "exito")
        self.assertIn("30654321090_20261027_DISTR-01", imp1.archivo.name)

        imp2 = importaciones[1]
        self.assertEqual(imp2.marca, self.marca2)
        self.assertEqual(imp2.cantidad, 1)
        self.assertEqual(imp2.estado, "exito")
        self.assertIn("30709876542_20261027_DISTR-02", imp2.archivo.name)

        # Verificar que se crearon los remitos atómicamente y en estado pendiente
        remitos_imp1 = Remito.objects.filter(importacion=imp1)
        self.assertEqual(remitos_imp1.count(), 2)
        for r in remitos_imp1:
            self.assertEqual(r.estado, EstadoRemito.PENDIENTE)
            self.assertIsNone(r.parada)
            self.assertEqual(r.marca, self.marca1)

        r1 = remitos_imp1.get(numero="0001-00001001")
        self.assertEqual(r1.total, Decimal("15000.50"))
        self.assertEqual(r1.comercio.cuit, "20301112223")
        self.assertEqual(r1.comercio.razon_social, "Kiosco Central")

        remitos_imp2 = Remito.objects.filter(importacion=imp2)
        self.assertEqual(remitos_imp2.count(), 1)
        r2 = remitos_imp2.first()
        self.assertEqual(r2.numero, "0002-00002001")
        self.assertEqual(r2.estado, EstadoRemito.PENDIENTE)
        self.assertEqual(r2.total, Decimal("35000.75"))

        # Limpiar archivos subidos en test
        imp1.archivo.delete(save=False)
        imp2.archivo.delete(save=False)

    def test_importar_remitos_fallback_a_marca_seleccionada(self):
        csv_content = (
            "cuit_comercio,condicion_iva,numero_iibb,razon_social,domicilio,monto_a_cobrar,fecha_factura,numero_sucursal,numero_factura\n"
            "20301112223,Monotributo,976-123456-1,Kiosco Central,\"Calle 1 123\",1000.00,2026-10-21,0001,00003001\n"
        ).encode("utf-8")
        file_sin_cuit_conocido = SimpleUploadedFile("archivo_random.csv", csv_content)
        response = self.client.post(
            reverse("remitos:importacion_crear"),
            {
                "archivo": [file_sin_cuit_conocido],
                "marca": self.marca1.id,
            },
        )
        self.assertRedirects(response, reverse("core:inicio"), fetch_redirect_response=False)

        imp = ImportacionRemitos.objects.get()
        self.assertEqual(imp.marca, self.marca1)
        self.assertEqual(imp.cantidad, 1)
        self.assertIn("archivo_random", imp.archivo.name)

        remito = Remito.objects.get(importacion=imp)
        self.assertEqual(remito.numero, "0001-00003001")
        self.assertEqual(remito.estado, EstadoRemito.PENDIENTE)
        self.assertEqual(remito.total, Decimal("1000.00"))
        imp.archivo.delete(save=False)

    def test_importar_remitos_con_errores_crea_error_importacion(self):
        csv_invalido = (
            "cuit_comercio,condicion_iva,numero_iibb,razon_social,domicilio,monto_a_cobrar,fecha_factura,numero_sucursal,numero_factura\n"
            "cuit_malo,Monotributo,976-123456-1,Kiosco Central,\"Calle 1 123\",-50.00,2026-10-21,0001,00004001\n"
            "20301112223,Monotributo,976-123456-1,Kiosco Central,\"Calle 1 123\",monto_invalido,2026-10-21,,00004002\n"
        ).encode("utf-8")
        archivo_erroneo = SimpleUploadedFile("30654321090_20261027_DISTR-01.csv", csv_invalido)

        response = self.client.post(
            reverse("remitos:importacion_crear"),
            {
                "archivo": [archivo_erroneo],
            },
        )
        self.assertRedirects(response, reverse("core:inicio"), fetch_redirect_response=False)

        importacion = ImportacionRemitos.objects.get()
        self.assertEqual(importacion.estado, EstadoImportacion.RECHAZADO)
        self.assertEqual(importacion.cantidad, 0)
        self.assertFalse(Remito.objects.filter(importacion=importacion).exists())

        errores = importacion.errores.order_by("fila")
        self.assertEqual(errores.count(), 2)

        err_fila2 = errores[0]
        self.assertEqual(err_fila2.fila, 2)
        self.assertIn("CUIT del comercio inválido", err_fila2.motivo)
        self.assertIn("El monto a cobrar debe ser mayor a cero", err_fila2.motivo)

        err_fila3 = errores[1]
        self.assertEqual(err_fila3.fila, 3)
        self.assertIn("Monto a cobrar inválido", err_fila3.motivo)
        self.assertIn("Falta número de sucursal", err_fila3.motivo)

        importacion.archivo.delete(save=False)

    def test_importar_remitos_reutiliza_comercio_por_cuit_sin_importar_diferencias_en_razon_o_domicilio(self):
        comercio_existente = Comercio.objects.create(
            cuit="20301112223",
            razon_social="Razón Social Original",
            domicilio="Domicilio Original 123",
        )
        csv_content = (
            "cuit_comercio,condicion_iva,numero_iibb,razon_social,domicilio,monto_a_cobrar,fecha_factura,numero_sucursal,numero_factura\n"
            "20301112223,Monotributo,976-123456-1,Razón Social Modificada O Distinta,\"Otro Domicilio 999\",1500.00,2026-10-21,0001,00005001\n"
        ).encode("utf-8")
        archivo = SimpleUploadedFile("30654321090_20261027_DISTR-01.csv", csv_content)

        response = self.client.post(
            reverse("remitos:importacion_crear"),
            {
                "archivo": [archivo],
            },
        )
        self.assertRedirects(response, reverse("core:inicio"), fetch_redirect_response=False)

        importacion = ImportacionRemitos.objects.get()
        self.assertEqual(importacion.estado, EstadoImportacion.EXITO)
        self.assertEqual(Comercio.objects.filter(cuit="20301112223").count(), 1)

        remito = Remito.objects.get(importacion=importacion)
        self.assertEqual(remito.comercio, comercio_existente)
        self.assertEqual(remito.comercio.razon_social, "Razón Social Original")
        importacion.archivo.delete(save=False)

    def test_importar_remitos_con_numeros_duplicados_crea_error_importacion(self):
        csv_con_duplicados = (
            "cuit_comercio,condicion_iva,numero_iibb,razon_social,domicilio,monto_a_cobrar,fecha_factura,numero_sucursal,numero_factura\n"
            "20301112223,Monotributo,976-123456-1,Kiosco Central,\"Calle 1 123\",500.00,2026-10-21,0001,00007777\n"
            "20301112223,Monotributo,976-123456-1,Kiosco Central,\"Calle 1 123\",600.00,2026-10-21,0001,00007777\n"
        ).encode("utf-8")
        archivo = SimpleUploadedFile("30654321090_20261027_DISTR-01.csv", csv_con_duplicados)

        response = self.client.post(
            reverse("remitos:importacion_crear"),
            {
                "archivo": [archivo],
            },
        )
        self.assertRedirects(response, reverse("core:inicio"), fetch_redirect_response=False)

        importacion = ImportacionRemitos.objects.get()
        self.assertEqual(importacion.estado, EstadoImportacion.RECHAZADO)
        errores = importacion.errores.all()
        self.assertEqual(errores.count(), 1)
        self.assertIn("duplicado", errores[0].motivo)
        importacion.archivo.delete(save=False)

    def test_importar_remitos_sin_razon_social_para_comercio_nuevo_es_rechazado(self):
        csv_sin_razon_social = (
            "cuit_comercio,condicion_iva,numero_iibb,razon_social,domicilio,monto_a_cobrar,fecha_factura,numero_sucursal,numero_factura\n"
            "20301112299,Monotributo,976-123456-1,,\"Calle Falsa 123\",500.00,2026-10-21,0001,00008888\n"
        ).encode("utf-8")
        archivo = SimpleUploadedFile("30654321090_20261027_DISTR-01.csv", csv_sin_razon_social)

        response = self.client.post(
            reverse("remitos:importacion_crear"),
            {
                "archivo": [archivo],
            },
        )
        self.assertRedirects(response, reverse("core:inicio"), fetch_redirect_response=False)

        importacion = ImportacionRemitos.objects.get()
        self.assertEqual(importacion.estado, EstadoImportacion.RECHAZADO)
        errores = importacion.errores.all()
        self.assertEqual(errores.count(), 1)
        self.assertIn("La razón social es obligatoria para comercios no registrados", errores[0].motivo)
        self.assertFalse(Comercio.objects.filter(cuit="20301112299").exists())
        importacion.archivo.delete(save=False)

    def test_importar_remitos_sin_razon_social_para_comercio_existente_es_aceptado(self):
        Comercio.objects.create(
            cuit="20301112288",
            razon_social="Comercio Preexistente",
            domicilio="Calle Real 456",
        )
        csv_sin_razon_social = (
            "cuit_comercio,condicion_iva,numero_iibb,razon_social,domicilio,monto_a_cobrar,fecha_factura,numero_sucursal,numero_factura\n"
            "20301112288,Monotributo,976-123456-1,,\"Calle Falsa 123\",500.00,2026-10-21,0001,00009999\n"
        ).encode("utf-8")
        archivo = SimpleUploadedFile("30654321090_20261027_DISTR-01.csv", csv_sin_razon_social)

        response = self.client.post(
            reverse("remitos:importacion_crear"),
            {
                "archivo": [archivo],
            },
        )
        self.assertRedirects(response, reverse("core:inicio"), fetch_redirect_response=False)

        importacion = ImportacionRemitos.objects.get()
        self.assertEqual(importacion.estado, EstadoImportacion.EXITO)
        remito = Remito.objects.get(numero="0001-00009999")
        self.assertEqual(remito.comercio.cuit, "20301112288")
        self.assertEqual(remito.comercio.razon_social, "Comercio Preexistente")
        importacion.archivo.delete(save=False)
