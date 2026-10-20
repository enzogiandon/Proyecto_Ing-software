from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (
    CrearUsuario,
    CustomLoginView,
    Inicio,
)

app_name = "core"

urlpatterns = [
    path("", Inicio.as_view(), name="inicio"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="core:login"), name="logout"),
    path("usuarios/crear", CrearUsuario.as_view(), name="crear_usuario"),
]

