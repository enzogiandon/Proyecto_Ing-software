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
