from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from .forms import EmpleadoCreateForm
from .models import Roles, Transportista


class EmpleadoViewsTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username="administrativo_autorizado",
            password="Testing-Password-123!",
            dni="12345678",
            rol=Roles.ADMINISTRATIVO,
        )
        permissions = Permission.objects.filter(
            content_type__app_label="core",
            codename__in=["view_usuario", "add_usuario", "change_usuario"],
        )
        self.user.user_permissions.add(*permissions)
        self.client.force_login(self.user)

    def test_create_administrative_employee_without_permissions(self):
        response = self.client.post(
            reverse("core:empleado_crear"),
            {
                "username": "nuevo_admin",
                "email": "admin@example.com",
                "first_name": "Ana",
                "last_name": "Pérez",
                "dni": "23456789",
                "telefono": "1112345678",
                "rol": Roles.ADMINISTRATIVO,
                "password": "Another-Secure-Password-42!",
                "password_confirm": "Another-Secure-Password-42!",
            },
        )

        self.assertRedirects(
            response,
            reverse("core:empleado_lista"),
            fetch_redirect_response=False,
        )
        employee = get_user_model().objects.get(username="nuevo_admin")
        self.assertTrue(employee.check_password("Another-Secure-Password-42!"))
        self.assertFalse(employee.user_permissions.exists())
        self.assertFalse(employee.groups.exists())
        self.assertEqual(
            [message.message for message in get_messages(response.wsgi_request)],
            ["Empleado registrado correctamente"],
        )

    def test_create_transportista_creates_profile(self):
        response = self.client.post(
            reverse("core:empleado_crear"),
            {
                "username": "nuevo_transportista",
                "email": "transporte@example.com",
                "first_name": "Luis",
                "last_name": "Gómez",
                "dni": "34567890",
                "telefono": "1112345678",
                "rol": Roles.TRANSPORTISTA,
                "password": "Transport-Password-42!",
                "password_confirm": "Transport-Password-42!",
            },
        )

        self.assertRedirects(
            response,
            reverse("core:empleado_lista"),
            fetch_redirect_response=False,
        )
        employee = get_user_model().objects.get(username="nuevo_transportista")
        self.assertTrue(Transportista.objects.filter(usuario=employee).exists())

    def test_duplicate_employee_dni_is_rejected(self):
        get_user_model().objects.create_user(
            username="empleado_existente",
            password="Existing-Password-42!",
            dni="45678901",
            rol=Roles.TRANSPORTISTA,
        )

        form = EmpleadoCreateForm(
            data={
                "username": "otro_usuario",
                "email": "otro@example.com",
                "first_name": "Otro",
                "last_name": "Empleado",
                "dni": "45678901",
                "telefono": "",
                "rol": Roles.ADMINISTRATIVO,
                "password": "Another-Secure-Password-42!",
                "password_confirm": "Another-Secure-Password-42!",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn(
            "El empleado ya se encuentra registrado.",
            form.errors["dni"],
        )
        self.assertFalse(
            get_user_model().objects.filter(username="otro_usuario").exists()
        )

    def test_update_employee_changes_profile_and_keeps_password(self):
        employee = get_user_model().objects.create_user(
            username="empleado",
            password="Original-Password-42!",
            dni="56789012",
            rol=Roles.TRANSPORTISTA,
        )

        response = self.client.post(
            reverse("core:empleado_editar", args=[employee.pk]),
            {
                "username": "empleado_actualizado",
                "email": "actualizado@example.com",
                "first_name": "Nombre",
                "last_name": "Actualizado",
                "dni": "56789012",
                "telefono": "1112345678",
                "rol": Roles.TRANSPORTISTA,
            },
        )

        self.assertRedirects(
            response,
            reverse("core:empleado_lista"),
            fetch_redirect_response=False,
        )
        employee.refresh_from_db()
        self.assertEqual(employee.first_name, "Nombre")
        self.assertTrue(employee.check_password("Original-Password-42!"))

    def test_suspend_employee_disables_account_without_deleting_it(self):
        employee = get_user_model().objects.create_user(
            username="empleado_a_suspender",
            password="Employee-Password-42!",
            dni="67890123",
            rol=Roles.TRANSPORTISTA,
        )

        response = self.client.post(
            reverse("core:empleado_suspender", args=[employee.pk])
        )

        self.assertRedirects(
            response,
            reverse("core:empleado_lista"),
            fetch_redirect_response=False,
        )
        employee.refresh_from_db()
        self.assertFalse(employee.is_active)
        self.assertTrue(
            get_user_model().objects.filter(pk=employee.pk).exists()
        )
        self.client.logout()
        self.assertFalse(
            self.client.login(
                username="empleado_a_suspender",
                password="Employee-Password-42!",
            )
        )
        self.assertEqual(
            [message.message for message in get_messages(response.wsgi_request)],
            ["Cuenta del empleado deshabilitada."],
        )

    def test_suspend_employee_does_not_change_account_on_get(self):
        employee = get_user_model().objects.create_user(
            username="empleado_sin_cambios",
            password="Employee-Password-42!",
            dni="78901234",
            rol=Roles.TRANSPORTISTA,
        )

        response = self.client.get(
            reverse("core:empleado_suspender", args=[employee.pk])
        )

        self.assertEqual(response.status_code, 405)
        employee.refresh_from_db()
        self.assertTrue(employee.is_active)


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

