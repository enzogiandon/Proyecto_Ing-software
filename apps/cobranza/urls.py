from django.urls import path

from .views import (
    AjustarCobranza,
    DetalleCobranza,
    ListaAjustesCobranza,
    ListaCobranza,
    ValidarCobranza,
)

app_name = "cobranza"

urlpatterns = [
    path("", ListaCobranza.as_view(), name="cobranza_lista"),
    path("<int:pk>/", DetalleCobranza.as_view(), name="cobranza_detalle"),
    path("<int:pk>/validar/", ValidarCobranza.as_view(), name="cobranza_validar"),
    path("<int:pk>/ajustar/", AjustarCobranza.as_view(), name="cobranza_ajustar"),
    path("ajustes/", ListaAjustesCobranza.as_view(), name="ajuste_lista"),
    # path("paradas/<int:pk>/", DetalleParada.as_view(), name="parada_detalle"),
    # path("crear/", CrearItinerarios.as_view(), name="itinerario_crear"),
    # path("paradas/crear/", CrearParadas.as_view(), name="paradas_crear"),
]

