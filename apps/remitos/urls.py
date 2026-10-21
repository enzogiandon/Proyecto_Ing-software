from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import (
    CrearMarca,
    CrearProducto,
    CrearRemito,
    DetalleImportacion,
    DetalleRemito,
    EditarMarca,
    EditarProducto,
    EditarRemito,
    EliminarImportacion,
    EliminarMarca,
    EliminarProducto,
    EliminarRemito,
    ImportarRemitos,
    ListaImportacion,
    ListaMarca,
    ListaProducto,
    ListaRemito,
)

app_name = "remitos"

urlpatterns = [
    path("", ListaRemito.as_view(), name="remito_lista"),
    path("nuevo/", CrearRemito.as_view(), name="remito_crear"),
    path("<int:pk>/editar/", EditarRemito.as_view(), name="remito_editar"),
    path("<int:pk>/", DetalleRemito.as_view(), name="remito_detalle"),
    path("<int:pk>/eliminar", EliminarRemito.as_view(), name="remito_eliminar"),

    path("importaciones/", ListaImportacion.as_view(), name="importacion_lista"),
    path("importaciones/nueva", ImportarRemitos.as_view(), name="importacion_crear"),
    path("importaciones/<int:pk>/", DetalleImportacion.as_view(), name="importacion_detalle"),
    path("importaciones/<int:pk>/eliminar", EliminarImportacion.as_view(), name="importacion_eliminar"),

    path("productos/", ListaProducto.as_view(), name="producto_lista"),
    path("productos/<int:pk>/editar", EditarProducto.as_view(), name="producto_editar"),
    path("productos/nuevo", CrearProducto.as_view(), name="producto_crear"),
    path("productos/<int:pk>/eliminar", EliminarProducto.as_view(), name="producto_eliminar"),

    path("marcas/", ListaMarca.as_view(), name="marca_lista"),
    path("marcas/<int:pk>/editar", EditarMarca.as_view(), name="marca_editar"),
    path("marcas/nuevo", CrearMarca.as_view(), name="marca_crear"),
    path("marcas/<int:pk>/eliminar", EliminarMarca.as_view(), name="marca_eliminar"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
