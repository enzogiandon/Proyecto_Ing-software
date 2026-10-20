from django.urls import path

from .views import (
    CrearRemito,
    DetalleRemito,
    EditarRemito,
    ImportarRemitos,
    ListaImportacion,
    ListaRemito,
)

app_name = "remitos"

urlpatterns = [
    path("lista/", ListaRemito.as_view(), name="remito_lista"),
    path("nuevo/", CrearRemito.as_view(), name="remito_crear"),
    path("<int:pk>/editar/", EditarRemito.as_view(), name="remito_editar"),
    path("<int:pk>/", DetalleRemito.as_view(), name="remito_detalle"),
    path("importaciones/", ListaImportacion.as_view(), name="importacion_lista"),
    path("importaciones/nueva", ImportarRemitos.as_view(), name="importacion_crear")
]
