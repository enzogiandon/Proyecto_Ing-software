from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (
    CrearEmpleado,
    CustomLoginView,
    EditarEmpleado,
    Inicio,
    ListaEmpleados,
)

app_name = "core"

urlpatterns = [
    path("", Inicio.as_view(), name="inicio"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="core:login"), name="logout"),
    path("empleados/", ListaEmpleados.as_view(), name="empleado_lista"),
    path("empleados/agregar/", CrearEmpleado.as_view(), name="empleado_crear"),
    path(
        "empleados/<int:pk>/editar/",
        EditarEmpleado.as_view(),
        name="empleado_editar",
    ),
    path("usuarios/crear", CrearEmpleado.as_view(), name="crear_usuario"),
]
