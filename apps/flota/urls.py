from django.urls import path

from .views import CrearVehiculo, EditarVehiculo, ListaVehiculos

app_name = "flota"

urlpatterns = [
    path("", ListaVehiculos.as_view(), name="vehiculo_lista"),
    path("nuevo/", CrearVehiculo.as_view(), name="vehiculo_crear"),
    path("<int:pk>/editar/", EditarVehiculo.as_view(), name="vehiculo_editar"),
]
