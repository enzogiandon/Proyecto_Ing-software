from django.urls import path

from .views import DetalleCobranza, ListaCobranza, ValidarCobranza

app_name = "cobranza"

urlpatterns = [
    path("", ListaCobranza.as_view(), name="cobranza_lista"),
    path("<int:pk>/", DetalleCobranza.as_view(), name="cobranza_detalle"),
    path("<int:pk>/validar/", ValidarCobranza.as_view(), name="cobranza_validar"),
    # path("paradas/<int:pk>/", DetalleParada.as_view(), name="parada_detalle"),
    # path("crear/", CrearItinerarios.as_view(), name="itinerario_crear"),
    # path("paradas/crear/", CrearParadas.as_view(), name="paradas_crear"),
]

