from datetime import date
from io import StringIO

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from apps.cobranza.models import Cobranza, EstadoCobranza
from apps.core.models import Grupos, Transportista, Vehiculo
from apps.itinerarios.models import (
    DetalleRutaGuardada,
    EstadoItinerario,
    EstadoParada,
    EvidenciaParada,
    Itinerario,
    Parada,
    ProblemaParada,
)
from apps.itinerarios.forms import CrearParadasForm
from apps.itinerarios.services import crear_itinerarios, crear_paradas
from apps.remitos.models import Comercio, EstadoRemito, Marca, Remito


class ItinerarioViewsTests(TestCase):
    def setUp(self):
        call_command("crear_grupos", stdout=StringIO())
        self.grupo_planificacion = Group.objects.get(
            name=Grupos.ADMIN_PLANIFICACION
        )
        self.grupo_transportista = Group.objects.get(name=Grupos.TRANSPORTISTA)

        user_model = get_user_model()
        self.administrativo = user_model.objects.create_user(
            username="11111111",
            password="Testing-Password-123!",
        )
        self.administrativo.groups.add(self.grupo_planificacion)
        self.client.force_login(self.administrativo)

        self.vehiculo = Vehiculo.objects.create(patente="AB123CD")
        self.transportista_user = user_model.objects.create_user(
            username="22222222",
            password="Driver-Password-123!",
        )
        self.transportista_user.groups.add(self.grupo_transportista)
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
        )
        second_user.groups.add(self.grupo_transportista)
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

    def test_create_itinerary_rejects_transportista_busy_on_date(self):
        second_vehiculo = Vehiculo.objects.create(patente="CD456EF")
        second_user = get_user_model().objects.create_user(
            username="33333333",
            password="Driver-Password-123!",
        )
        second_user.groups.add(self.grupo_transportista)
        second_transportista = Transportista.objects.create(
            usuario=second_user,
            vehiculo=second_vehiculo,
        )
        Itinerario.objects.create(
            fecha=date(2026, 10, 25),
            transportista=self.transportista,
            vehiculo=self.vehiculo,
            estado=EstadoItinerario.ASIGNADO,
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

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "ya tiene un itinerario asignado para la fecha indicada"
        )
        self.assertEqual(Itinerario.objects.count(), 1)

    def test_create_itinerary_allows_same_transportista_on_other_date(self):
        Itinerario.objects.create(
            fecha=date(2026, 10, 25),
            transportista=self.transportista,
            vehiculo=self.vehiculo,
            estado=EstadoItinerario.ASIGNADO,
        )

        response = self.client.post(
            reverse("itinerarios:itinerario_crear"),
            {"fecha": "2026-10-26", "transportistas": [self.transportista.pk]},
        )

        self.assertRedirects(
            response,
            reverse("itinerarios:itinerario_lista"),
            fetch_redirect_response=False,
        )
        self.assertEqual(Itinerario.objects.count(), 2)

    def test_crear_itinerarios_service_rejects_busy_transportista(self):
        Itinerario.objects.create(
            fecha=date(2026, 10, 25),
            transportista=self.transportista,
            vehiculo=self.vehiculo,
            estado=EstadoItinerario.ASIGNADO,
        )

        with self.assertRaisesMessage(
            ValidationError,
            f"El transportista {self.transportista} ya tiene un itinerario "
            "asignado para el 25/10/2026.",
        ):
            crear_itinerarios([self.transportista], date(2026, 10, 25))
        self.assertEqual(Itinerario.objects.count(), 1)

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

    def test_modificar_paradas_desmarca_y_marca_nuevas(self):
        itinerario = Itinerario.objects.create(
            fecha=date(2026, 10, 25),
            transportista=self.transportista,
            vehiculo=self.vehiculo,
            estado=EstadoItinerario.ASIGNADO,
        )
        comercio_1 = self.crear_comercio("Comercio 1", "20123456791")
        comercio_2 = self.crear_comercio("Comercio 2", "20123456792")
        comercio_3 = self.crear_comercio("Comercio 3", "20123456793")

        remito_1 = self.crear_remito(comercio_1, "R-101")
        remito_2 = self.crear_remito(comercio_2, "R-102")
        remito_3 = self.crear_remito(comercio_3, "R-103")

        # 1. Asignar comercio 1 y 2
        crear_paradas(itinerario, [comercio_1, comercio_2])
        self.assertEqual(itinerario.paradas.count(), 2)

        # 2. Desmarcar comercio 1, mantener comercio 2, y agregar comercio 3
        crear_paradas(itinerario, [comercio_2, comercio_3])

        remito_1.refresh_from_db()
        remito_2.refresh_from_db()
        remito_3.refresh_from_db()

        self.assertEqual(remito_1.estado, EstadoRemito.PENDIENTE)
        self.assertIsNone(remito_1.parada)

        self.assertEqual(remito_2.estado, EstadoRemito.ASIGNADO)
        self.assertIsNotNone(remito_2.parada)

        self.assertEqual(remito_3.estado, EstadoRemito.ASIGNADO)
        self.assertIsNotNone(remito_3.parada)

        self.assertEqual(itinerario.paradas.count(), 2)
        paradas = list(itinerario.paradas.order_by("orden"))
        self.assertEqual(paradas[0].comercio, comercio_2)
        self.assertEqual(paradas[0].orden, 1)
        self.assertEqual(paradas[1].comercio, comercio_3)
        self.assertEqual(paradas[1].orden, 2)

    def test_crear_paradas_con_seleccion_granular_de_remitos(self):
        itinerario = Itinerario.objects.create(
            fecha=date(2026, 10, 25),
            transportista=self.transportista,
            vehiculo=self.vehiculo,
            estado=EstadoItinerario.ASIGNADO,
        )
        comercio = self.crear_comercio("Comercio Granular", "20123456794")
        remito_1 = self.crear_remito(comercio, "R-GRAN-1")
        remito_2 = self.crear_remito(comercio, "R-GRAN-2")
        remito_3 = self.crear_remito(comercio, "R-GRAN-3")

        # Seleccionar solo 2 de los 3 remitos (cherry-picking)
        crear_paradas(itinerario, remitos=[remito_1, remito_2])

        self.assertEqual(itinerario.paradas.count(), 1)
        parada = itinerario.paradas.first()
        self.assertEqual(parada.comercio, comercio)

        remito_1.refresh_from_db()
        remito_2.refresh_from_db()
        remito_3.refresh_from_db()

        self.assertEqual(remito_1.parada, parada)
        self.assertEqual(remito_1.estado, EstadoRemito.ASIGNADO)
        self.assertEqual(remito_2.parada, parada)
        self.assertEqual(remito_2.estado, EstadoRemito.ASIGNADO)

        # El tercer remito no seleccionado debe permanecer pendiente y sin parada
        self.assertIsNone(remito_3.parada)
        self.assertEqual(remito_3.estado, EstadoRemito.PENDIENTE)

    def test_dividir_remitos_del_mismo_comercio_en_dos_itinerarios(self):
        itinerario_1 = Itinerario.objects.create(
            fecha=date(2026, 10, 25),
            transportista=self.transportista,
            vehiculo=self.vehiculo,
            estado=EstadoItinerario.ASIGNADO,
        )
        itinerario_2 = Itinerario.objects.create(
            fecha=date(2026, 10, 26),
            transportista=self.transportista,
            vehiculo=self.vehiculo,
            estado=EstadoItinerario.ASIGNADO,
        )
        comercio = self.crear_comercio("Comercio Split", "20123456795")
        remito_lunes = self.crear_remito(comercio, "R-SPLIT-LUNES")
        remito_martes = self.crear_remito(comercio, "R-SPLIT-MARTES")

        # Asignar R-SPLIT-LUNES a itinerario 1
        crear_paradas(itinerario_1, remitos=[remito_lunes])
        # Asignar R-SPLIT-MARTES a itinerario 2
        crear_paradas(itinerario_2, remitos=[remito_martes])

        self.assertEqual(itinerario_1.paradas.count(), 1)
        self.assertEqual(itinerario_2.paradas.count(), 1)

        parada_1 = itinerario_1.paradas.first()
        parada_2 = itinerario_2.paradas.first()

        self.assertNotEqual(parada_1.pk, parada_2.pk)
        self.assertEqual(parada_1.comercio, comercio)
        self.assertEqual(parada_2.comercio, comercio)

        remito_lunes.refresh_from_db()
        remito_martes.refresh_from_db()

        self.assertEqual(remito_lunes.parada, parada_1)
        self.assertEqual(remito_lunes.estado, EstadoRemito.ASIGNADO)
        self.assertEqual(remito_martes.parada, parada_2)
        self.assertEqual(remito_martes.estado, EstadoRemito.ASIGNADO)

    def test_desasignar_remito_especifico_al_actualizar_parada(self):
        itinerario = Itinerario.objects.create(
            fecha=date(2026, 10, 25),
            transportista=self.transportista,
            vehiculo=self.vehiculo,
            estado=EstadoItinerario.ASIGNADO,
        )
        comercio = self.crear_comercio("Comercio Update", "20123456796")
        remito_1 = self.crear_remito(comercio, "R-UPD-1")
        remito_2 = self.crear_remito(comercio, "R-UPD-2")

        # Asignar ambos inicialmente
        crear_paradas(itinerario, remitos=[remito_1, remito_2])
        self.assertEqual(itinerario.paradas.count(), 1)
        parada = itinerario.paradas.first()

        # Actualizar dejando solo remito_1
        crear_paradas(itinerario, remitos=[remito_1])

        self.assertEqual(itinerario.paradas.count(), 1)
        remito_1.refresh_from_db()
        remito_2.refresh_from_db()

        self.assertEqual(remito_1.parada, parada)
        self.assertEqual(remito_1.estado, EstadoRemito.ASIGNADO)
        self.assertIsNone(remito_2.parada)
        self.assertEqual(remito_2.estado, EstadoRemito.PENDIENTE)

    def test_crear_paradas_desmarcar_todos_remitos_elimina_parada(self):
        itinerario = Itinerario.objects.create(
            fecha=date(2026, 10, 25),
            transportista=self.transportista,
            vehiculo=self.vehiculo,
            estado=EstadoItinerario.ASIGNADO,
        )
        comercio_1 = self.crear_comercio("Comercio Del-1", "20123456797")
        comercio_2 = self.crear_comercio("Comercio Del-2", "20123456798")
        remito_1 = self.crear_remito(comercio_1, "R-DEL-1")
        remito_2 = self.crear_remito(comercio_2, "R-DEL-2")

        crear_paradas(itinerario, remitos=[remito_1, remito_2])
        self.assertEqual(itinerario.paradas.count(), 2)

        # Desmarcar comercio 1 por completo, pasando solo remito_2
        crear_paradas(itinerario, remitos=[remito_2])

        self.assertEqual(itinerario.paradas.count(), 1)
        remito_1.refresh_from_db()
        remito_2.refresh_from_db()

        self.assertIsNone(remito_1.parada)
        self.assertEqual(remito_1.estado, EstadoRemito.PENDIENTE)
        self.assertIsNotNone(remito_2.parada)
        self.assertEqual(remito_2.estado, EstadoRemito.ASIGNADO)

    def test_form_paradas_builds_comercios_agrupados_tri_state(self):
        itinerario = Itinerario.objects.create(
            fecha=date(2026, 10, 25),
            transportista=self.transportista,
            vehiculo=self.vehiculo,
            estado=EstadoItinerario.ASIGNADO,
        )
        comercio = self.crear_comercio("Comercio Form", "20123456799")
        remito_1 = self.crear_remito(comercio, "R-FORM-1")
        remito_2 = self.crear_remito(comercio, "R-FORM-2")

        # 1. Sin seleccionar (unbound)
        form = CrearParadasForm(itinerario_id=itinerario.pk)
        self.assertEqual(len(form.comercios_agrupados), 1)
        grupo = form.comercios_agrupados[0]
        self.assertEqual(grupo["total_count"], 2)
        self.assertEqual(grupo["selected_count"], 0)
        self.assertFalse(grupo["all_selected"])
        self.assertFalse(grupo["is_indeterminate"])

        # 2. Selección parcial (bound) -> Indeterminate
        bound_form = CrearParadasForm(
            data={"itinerario": itinerario.pk, "remitos": [remito_1.pk]},
            itinerario_id=itinerario.pk,
        )
        self.assertTrue(bound_form.is_valid())
        grupo_bound = bound_form.comercios_agrupados[0]
        self.assertEqual(grupo_bound["selected_count"], 1)
        self.assertFalse(grupo_bound["all_selected"])
        self.assertTrue(grupo_bound["is_indeterminate"])

        # 3. Selección completa (bound) -> All selected
        all_form = CrearParadasForm(
            data={"itinerario": itinerario.pk, "remitos": [remito_1.pk, remito_2.pk]},
            itinerario_id=itinerario.pk,
        )
        self.assertTrue(all_form.is_valid())
        grupo_all = all_form.comercios_agrupados[0]
        self.assertEqual(grupo_all["selected_count"], 2)
        self.assertTrue(grupo_all["all_selected"])
        self.assertFalse(grupo_all["is_indeterminate"])

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

    def test_post_quitar_remito_from_parada(self):
        itinerario = Itinerario.objects.create(
            fecha=date(2026, 10, 25),
            transportista=self.transportista,
            vehiculo=self.vehiculo,
            estado=EstadoItinerario.ASIGNADO,
        )
        comercio = self.crear_comercio("Comercio Quitar", "20123456795")
        parada = Parada.objects.create(
            itinerario=itinerario,
            comercio=comercio,
            orden=1,
            estado=EstadoParada.PENDIENTE,
        )
        remito_1 = self.crear_remito(comercio, "R-QUIT-001")
        remito_1.parada = parada
        remito_1.estado = EstadoRemito.ASIGNADO
        remito_1.save()

        remito_2 = self.crear_remito(comercio, "R-QUIT-002")
        remito_2.parada = parada
        remito_2.estado = EstadoRemito.ASIGNADO
        remito_2.save()

        response = self.client.post(
            reverse("itinerarios:parada_detalle", args=[parada.pk]),
            {"accion": "quitar_remito", "remito_id": remito_1.pk},
        )

        self.assertRedirects(
            response,
            reverse("itinerarios:parada_detalle", args=[parada.pk]),
        )
        remito_1.refresh_from_db()
        self.assertIsNone(remito_1.parada)
        self.assertEqual(remito_1.estado, EstadoRemito.PENDIENTE)
        self.assertTrue(Parada.objects.filter(pk=parada.pk).exists())

        # Al quitar el último remito, la parada debe eliminarse
        response_last = self.client.post(
            reverse("itinerarios:parada_detalle", args=[parada.pk]),
            {"accion": "quitar_remito", "remito_id": remito_2.pk},
        )
        self.assertRedirects(
            response_last,
            reverse("itinerarios:itinerario_lista"),
        )
        remito_2.refresh_from_db()
        self.assertIsNone(remito_2.parada)
        self.assertEqual(remito_2.estado, EstadoRemito.PENDIENTE)
        self.assertFalse(Parada.objects.filter(pk=parada.pk).exists())

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
        content = response.content.decode().split("Entregas y paradas", 1)[1]
        positions = [
            content.index(f">{parada.comercio.razon_social}<")
            for parada in [paradas[1], paradas[0], paradas[2], paradas[3]]
        ]
        self.assertEqual(positions, sorted(positions))

    def test_delete_itinerary_resets_remitos_to_pending(self):
        itinerario = Itinerario.objects.create(
            fecha=date(2026, 10, 25),
            transportista=self.transportista,
            vehiculo=self.vehiculo,
            estado=EstadoItinerario.ASIGNADO,
        )
        comercio = self.crear_comercio("Comercio Eliminar", "20123456799")
        parada = Parada.objects.create(
            itinerario=itinerario,
            comercio=comercio,
            orden=1,
            estado=EstadoParada.PENDIENTE,
        )
        remito = self.crear_remito(comercio, "R-DEL-001")
        remito.parada = parada
        remito.estado = EstadoRemito.ASIGNADO
        remito.save()

        response = self.client.post(
            reverse("itinerarios:itinerario_eliminar", args=[itinerario.pk])
        )
        self.assertRedirects(response, reverse("itinerarios:itinerario_lista"))
        self.assertFalse(Itinerario.objects.filter(pk=itinerario.pk).exists())
        remito.refresh_from_db()
        self.assertIsNone(remito.parada)
        self.assertEqual(remito.estado, EstadoRemito.PENDIENTE)

    def test_delete_itinerary_with_cobranza_is_rejected(self):
        itinerario = Itinerario.objects.create(
            fecha=date(2026, 10, 24),
            transportista=self.transportista,
            vehiculo=self.vehiculo,
            estado=EstadoItinerario.ASIGNADO,
        )
        comercio = Comercio.objects.create(
            cuit="20123456782",
            razon_social="Comercio Con Cobranza",
            domicilio="Av. Siempre Viva 742",
        )
        parada = Parada.objects.create(
            itinerario=itinerario,
            comercio=comercio,
            orden=1,
            estado=EstadoParada.PENDIENTE,
        )
        remito = self.crear_remito(comercio, "R-DEL-COB-01")
        remito.parada = parada
        remito.estado = EstadoRemito.ASIGNADO
        remito.save()
        Cobranza.objects.create(parada=parada, estado=EstadoCobranza.REGISTRADO)

        response = self.client.post(
            reverse("itinerarios:itinerario_eliminar", args=[itinerario.pk]),
            follow=True,
        )
        self.assertRedirects(response, reverse("itinerarios:itinerario_lista"))
        # El itinerario NO debe eliminarse para preservar la trazabilidad contable
        self.assertTrue(Itinerario.objects.filter(pk=itinerario.pk).exists())
        self.assertContains(
            response,
            "No se puede eliminar el itinerario porque posee cobranzas o rendiciones registradas.",
        )

    def test_delete_nonexistent_itinerary_shows_error(self):
        response = self.client.post(
            reverse("itinerarios:itinerario_eliminar", args=[99999]),
            follow=True,
        )
        self.assertContains(response, "Itinerario no encontrado")

    def test_edit_itinerary_transportista_scenarios(self):
        itinerario = Itinerario.objects.create(
            fecha=date(2026, 10, 25),
            transportista=self.transportista,
            vehiculo=self.vehiculo,
            estado=EstadoItinerario.ASIGNADO,
        )

        response_unassign = self.client.post(
            reverse("itinerarios:itinerario_editar", args=[itinerario.pk]),
            {
                "accion": "guardar_cambios",
                "fecha": "2026-10-25",
                "transportista": "",
                "vehiculo": "",
            },
            follow=True,
        )
        itinerario.refresh_from_db()
        self.assertIsNone(itinerario.transportista)
        self.assertEqual(itinerario.estado, EstadoItinerario.PENDIENTE)
        self.assertContains(response_unassign, "Transportista asignado con éxito")

        response_assign = self.client.post(
            reverse("itinerarios:itinerario_editar", args=[itinerario.pk]),
            {
                "accion": "guardar_cambios",
                "fecha": "2026-10-25",
                "transportista": str(self.transportista.pk),
                "vehiculo": str(self.vehiculo.pk),
            },
            follow=True,
        )
        itinerario.refresh_from_db()
        self.assertEqual(itinerario.transportista, self.transportista)
        self.assertEqual(itinerario.estado, EstadoItinerario.ASIGNADO)
        self.assertContains(response_assign, "Transportista asignado con éxito")

        second_vehiculo = Vehiculo.objects.create(patente="ZZ999ZZ")
        second_user = get_user_model().objects.create_user(
            username="44444444",
            password="Driver-Password-123!",
        )
        second_user.groups.add(self.grupo_transportista)
        second_transportista = Transportista.objects.create(
            usuario=second_user,
            vehiculo=second_vehiculo,
        )
        Itinerario.objects.create(
            fecha=date(2026, 10, 25),
            transportista=second_transportista,
            vehiculo=second_vehiculo,
            estado=EstadoItinerario.ASIGNADO,
        )

        response_fail = self.client.post(
            reverse("itinerarios:itinerario_editar", args=[itinerario.pk]),
            {
                "accion": "guardar_cambios",
                "fecha": "2026-10-25",
                "transportista": str(second_transportista.pk),
            },
            follow=True,
        )
        itinerario.refresh_from_db()
        self.assertEqual(itinerario.transportista, self.transportista)
        self.assertContains(response_fail, "Transportista no asignado")


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
