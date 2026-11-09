from io import StringIO

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.messages import get_messages
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from apps.core.forms import EmpleadoCreateForm
from apps.core.models import EstadoVehiculo, Grupos, Transportista, Vehiculo


class EmpleadoViewsTests(TestCase):
    def setUp(self):
        call_command("crear_grupos", stdout=StringIO())
        self.gestion_personal = Group.objects.get(name=Grupos.GESTION_PERSONAL)
        self.grupo_transportista = Group.objects.get(name=Grupos.TRANSPORTISTA)

        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username="11111111",
            password="Admin-Password-42!",
        )
        self.user.groups.add(self.gestion_personal)
        self.client.force_login(self.user)

    def test_create_employee_assigns_selected_group_without_direct_permissions(self):
        response = self.client.post(
            reverse("core:empleado_crear"),
            {
                "username": "23456789",
                "email": "admin@example.com",
                "first_name": "Ana",
                "last_name": "Pérez",
                "telefono": "1112345678",
                "grupos": [self.gestion_personal.pk],
                "password": "Another-Secure-Password-42!",
                "password_confirm": "Another-Secure-Password-42!",
            },
        )

        self.assertRedirects(
            response,
            reverse("core:empleado_lista"),
            fetch_redirect_response=False,
        )
        employee = get_user_model().objects.get(username="23456789")
        self.assertTrue(employee.check_password("Another-Secure-Password-42!"))
        self.assertQuerySetEqual(employee.groups.all(), [self.gestion_personal])
        self.assertFalse(employee.user_permissions.exists())
        self.assertEqual(
            [message.message for message in get_messages(response.wsgi_request)],
            ["Empleado registrado correctamente"],
        )

    def test_create_transportista_assigns_group_and_creates_profile(self):
        response = self.client.post(
            reverse("core:empleado_crear"),
            {
                "username": "34567890",
                "email": "transporte@example.com",
                "first_name": "Luis",
                "last_name": "Gómez",
                "telefono": "1112345678",
                "grupos": [self.grupo_transportista.pk],
                "password": "Transport-Password-42!",
                "password_confirm": "Transport-Password-42!",
            },
        )

        self.assertRedirects(
            response,
            reverse("core:empleado_lista"),
            fetch_redirect_response=False,
        )
        employee = get_user_model().objects.get(username="34567890")
        self.assertTrue(Transportista.objects.filter(usuario=employee).exists())
        self.assertQuerySetEqual(employee.groups.all(), [self.grupo_transportista])

    def test_duplicate_employee_dni_is_rejected(self):
        get_user_model().objects.create_user(
            username="45678901",
            password="Original-Password-42!",
        )

        form = EmpleadoCreateForm(
            data={
                "username": "45678901",
                "email": "otro@example.com",
                "first_name": "Otro",
                "last_name": "Empleado",
                "telefono": "",
                "grupos": [self.gestion_personal.pk],
                "password": "Another-Secure-Password-42!",
                "password_confirm": "Another-Secure-Password-42!",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn(
            "El empleado ya se encuentra registrado.",
            form.errors["username"],
        )
        self.assertEqual(
            get_user_model().objects.filter(username="45678901").count(), 1
        )

    def test_update_employee_changes_group_and_keeps_password(self):
        employee = get_user_model().objects.create_user(
            username="56789012",
            password="Original-Password-42!",
            first_name="Nombre",
            last_name="Anterior",
        )
        employee.groups.add(self.grupo_transportista)
        Transportista.objects.create(usuario=employee)

        response = self.client.post(
            reverse("core:empleado_editar", args=[employee.pk]),
            {
                "username": "56789013",
                "email": "actualizado@example.com",
                "first_name": "Nombre actualizado",
                "last_name": "Apellido actualizado",
                "telefono": "1112345678",
                "grupos": [self.gestion_personal.pk],
                "password": "",
                "password_confirm": "",
            },
        )

        self.assertRedirects(
            response,
            reverse("core:empleado_lista"),
            fetch_redirect_response=False,
        )
        employee.refresh_from_db()
        self.assertEqual(employee.email, "actualizado@example.com")
        self.assertEqual(employee.username, "56789012")
        self.assertEqual(employee.first_name, "Nombre")
        self.assertTrue(employee.check_password("Original-Password-42!"))
        self.assertQuerySetEqual(employee.groups.all(), [self.gestion_personal])
        self.assertFalse(Transportista.objects.filter(usuario=employee).exists())

    def test_suspend_employee_disables_account_without_deleting_it(self):
        employee = get_user_model().objects.create_user(
            username="67890123",
            password="Original-Password-42!",
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
        self.assertTrue(get_user_model().objects.filter(pk=employee.pk).exists())
        self.client.logout()
        self.assertFalse(
            self.client.login(
                username="67890123",
                password="Original-Password-42!",
            )
        )
        self.assertEqual(
            [message.message for message in get_messages(response.wsgi_request)],
            ["Cuenta del empleado deshabilitada."],
        )

    def test_suspend_employee_does_not_change_account_on_get(self):
        employee = get_user_model().objects.create_user(
            username="78901234",
            password="Original-Password-42!",
        )

        response = self.client.get(
            reverse("core:empleado_suspender", args=[employee.pk])
        )

        self.assertEqual(response.status_code, 405)
        employee.refresh_from_db()
        self.assertTrue(employee.is_active)

    def test_reset_employee_credentials_reactivates_account_and_changes_password(self):
        employee = get_user_model().objects.create_user(
            username="89012345",
            password="Original-Password-42!",
        )
        employee.is_active = False
        employee.save(update_fields=["is_active"])

        response = self.client.post(
            reverse("core:empleado_restablecer_credenciales", args=[employee.pk]),
            {
                "password": "Nueva-Password-42!",
                "password_confirm": "Nueva-Password-42!",
            },
        )

        self.assertRedirects(
            response,
            reverse("core:empleado_lista"),
            fetch_redirect_response=False,
        )
        employee.refresh_from_db()
        self.assertTrue(employee.is_active)
        self.assertTrue(employee.check_password("Nueva-Password-42!"))
        self.assertEqual(
            [message.message for message in get_messages(response.wsgi_request)],
            ["Credenciales restablecidas correctamente."],
        )


class VehiculoViewsTests(TestCase):
    def setUp(self):
        call_command("crear_grupos", stdout=StringIO())
        self.gestion_personal = Group.objects.get(name=Grupos.GESTION_PERSONAL)

        self.user = get_user_model().objects.create_user(
            username="12345678",
            password="Vehiculo-Password-42!",
        )
        self.user.groups.add(self.gestion_personal)
        self.client.force_login(self.user)

    def test_create_vehicle_redirects_to_list_and_shows_success(self):
        response = self.client.post(
            reverse("core:vehiculo_crear"),
            {
                "patente": "ab123cd",
                "modelo": "Camión de reparto",
                "poliza": "POL-123",
                "estado": EstadoVehiculo.DISPONIBLE,
            },
        )

        self.assertRedirects(
            response,
            reverse("core:vehiculo_lista"),
            fetch_redirect_response=False,
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
            reverse("core:vehiculo_crear"),
            {
                "patente": "ab123cd",
                "modelo": "Otro camión",
                "poliza": "",
                "estado": EstadoVehiculo.DISPONIBLE,
            },
        )

        self.assertRedirects(
            response,
            reverse("core:vehiculo_lista"),
            fetch_redirect_response=False,
        )
        self.assertEqual(Vehiculo.objects.count(), 1)
        self.assertEqual(
            [message.message for message in get_messages(response.wsgi_request)],
            ["Vehículo repetido"],
        )

    def test_update_vehicle_changes_state_and_shows_success(self):
        vehiculo = Vehiculo.objects.create(patente="AB123CD")

        response = self.client.post(
            reverse("core:vehiculo_editar", args=[vehiculo.pk]),
            {
                "patente": "ab123cd",
                "modelo": "Camión actualizado",
                "poliza": "POL-456",
                "estado": EstadoVehiculo.NO_OPERATIVO,
            },
        )

        self.assertRedirects(
            response,
            reverse("core:vehiculo_lista"),
            fetch_redirect_response=False,
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

        response = self.client.get(reverse("core:vehiculo_crear"))

        self.assertRedirects(
            response,
            f"{reverse('core:login')}?next={reverse('core:vehiculo_crear')}",
            fetch_redirect_response=False,
        )
