from decimal import Decimal

from django.test import TestCase

from apps.cobranza.forms import DetallePagoFormSet, DetallePagoValidarForm
from apps.cobranza.models import Cobranza, DetallePago, EstadoCobranza, MedioPago
from apps.itinerarios.models import EstadoItinerario, EstadoParada, Itinerario, Parada
from apps.remitos.models import Comercio


class DetallePagoValidarTests(TestCase):
    def setUp(self):
        self.comercio = Comercio.objects.create(
            razon_social="Comercio Cobranza",
            cuit="30112233445",
            domicilio="Calle 123",
        )
        self.itinerario = Itinerario.objects.create(
            fecha="2026-11-15",
            estado=EstadoItinerario.ASIGNADO,
        )
        self.parada = Parada.objects.create(
            itinerario=self.itinerario,
            comercio=self.comercio,
            orden=1,
            estado=EstadoParada.FINALIZADA,
        )
        self.cobranza = Cobranza.objects.create(
            parada=self.parada,
            estado=EstadoCobranza.REGISTRADO,
        )
        self.detalle_con_none = DetallePago.objects.create(
            cobranza=self.cobranza,
            medio=MedioPago.TRANSFERENCIA,
            monto_declarado=Decimal("500.00"),
            monto_verificado=None,
        )

    def test_form_cleans_empty_monto_verificado_to_zero(self):
        form = DetallePagoValidarForm(
            data={"monto_verificado": "", "id": self.detalle_con_none.id, "cobranza": self.cobranza.id},
            instance=self.detalle_con_none,
        )
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["monto_verificado"], Decimal("0.00"))
        self.assertTrue(form.has_changed())
        self.assertIn("monto_verificado", form.changed_data)

    def test_formset_saves_zero_when_monto_verificado_is_empty_and_was_none(self):
        data = {
            "detalles-TOTAL_FORMS": "1",
            "detalles-INITIAL_FORMS": "1",
            "detalles-MIN_NUM_FORMS": "0",
            "detalles-MAX_NUM_FORMS": "1000",
            "detalles-0-id": str(self.detalle_con_none.id),
            "detalles-0-monto_verificado": "",
        }
        formset = DetallePagoFormSet(data=data, instance=self.cobranza)
        self.assertTrue(formset.is_valid(), formset.errors)

        formset.save()
        self.detalle_con_none.refresh_from_db()
        self.assertEqual(self.detalle_con_none.monto_verificado, Decimal("0.00"))

