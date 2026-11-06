from django.urls import path

from .views import CrearItinerarios, CrearParadas, DetalleParada, ListaItinerarios

app_name = "itinerarios"

urlpatterns = [
    path("", ListaItinerarios.as_view(), name="itinerario_lista"),
    path("paradas/<int:pk>/", DetalleParada.as_view(), name="parada_detalle"),
    path("crear/", CrearItinerarios.as_view(), name="itinerario_crear"),
    path("paradas/crear/", CrearParadas.as_view(), name="paradas_crear"),
]
