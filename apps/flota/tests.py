from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from .models import EstadoVehiculo, Vehiculo


class VehiculoViewsTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username="administrativo",
            password="test-password",
            dni="12345678",
            rol="administrativo",
        )
        self.add_permission = Permission.objects.get(
            content_type__app_label="flota", codename="add_vehiculo"
        )
        self.change_permission = Permission.objects.get(
            content_type__app_label="flota", codename="change_vehiculo"
        )
        self.view_permission = Permission.objects.get(
            content_type__app_label="flota", codename="view_vehiculo"
        )
        self.user.user_permissions.add(
            self.add_permission, self.change_permission, self.view_permission
        )
        self.client.force_login(self.user)

    def test_create_vehicle_redirects_to_list_and_shows_success(self):
        response = self.client.post(
            reverse("flota:vehiculo_crear"),
            {
                "patente": "ab123cd",
                "modelo": "Camión de reparto",
                "poliza": "POL-123",
                "estado": EstadoVehiculo.DISPONIBLE,
            },
        )

        self.assertRedirects(
            response, reverse("flota:vehiculo_lista"), fetch_redirect_response=False
        )
        self.assertTrue(
            Vehiculo.objects.filter(
                patente="AB123CD", estado=EstadoVehiculo.DISPONIBLE
            ).exists()
        )
        self.assertEqual(
            [message.message for message in get_messages(response.wsgi_request)],
            ["Vehículo registrado exitosamente"],
        )

    def test_duplicate_plate_redirects_to_list_and_shows_error(self):
        Vehiculo.objects.create(patente="AB123CD")

        response = self.client.post(
            reverse("flota:vehiculo_crear"),
            {
                "patente": "ab123cd",
                "modelo": "Otro camión",
                "poliza": "",
                "estado": EstadoVehiculo.DISPONIBLE,
            },
        )

        self.assertRedirects(
            response, reverse("flota:vehiculo_lista"), fetch_redirect_response=False
        )
        self.assertEqual(Vehiculo.objects.count(), 1)
        self.assertEqual(
            [message.message for message in get_messages(response.wsgi_request)],
            ["Vehículo repetido"],
        )

    def test_update_vehicle_changes_state_and_shows_success(self):
        vehiculo = Vehiculo.objects.create(patente="AB123CD")

        response = self.client.post(
            reverse("flota:vehiculo_editar", args=[vehiculo.pk]),
            {
                "patente": "ab123cd",
                "modelo": "Camión actualizado",
                "poliza": "POL-456",
                "estado": EstadoVehiculo.NO_OPERATIVO,
            },
        )

        self.assertRedirects(
            response, reverse("flota:vehiculo_lista"), fetch_redirect_response=False
        )
        vehiculo.refresh_from_db()
        self.assertEqual(vehiculo.modelo, "Camión actualizado")
        self.assertEqual(vehiculo.estado, EstadoVehiculo.NO_OPERATIVO)
        self.assertEqual(
            [message.message for message in get_messages(response.wsgi_request)],
            ["Vehículo modificado exitosamente"],
        )

    def test_create_vehicle_requires_login(self):
        self.client.logout()

        response = self.client.get(reverse("flota:vehiculo_crear"))

        self.assertRedirects(
            response,
            f"{reverse('core:login')}?next={reverse('flota:vehiculo_crear')}",
            fetch_redirect_response=False,
        )
