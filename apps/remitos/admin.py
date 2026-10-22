from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import (
    Comercio,
    ErrorImportacion,
    ImportacionRemitos,
    ItemRemito,
    Marca,
    Producto,
    Remito,
)


# ---------------------------------------------------------
# Inlines: para ver/cargar elementos relacionados adentro del padre
# ---------------------------------------------------------
class ItemRemitoInline(admin.TabularInline):
  model = ItemRemito
  extra = 1
  autocomplete_fields = ["producto"]


class ErrorImportacionInline(admin.TabularInline):
  model = ErrorImportacion
  extra = 0
  readonly_fields = ("fila", "motivo")
  can_delete = False


# ---------------------------------------------------------
# ModelAdmins
# ---------------------------------------------------------
@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
  list_display = ("nombre", "cuit", "telefono", "email", "activo")
  list_filter = ("activo",)
  search_fields = ("nombre", "cuit", "email")


@admin.register(Comercio)
class ComercioAdmin(admin.ModelAdmin):
  list_display = ("razon_social", "cuit", "domicilio", "telefono", "activo")
  list_filter = ("activo",)
  search_fields = ("razon_social", "cuit", "domicilio")


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
  list_display = ("nombre", "codigo", "marca", "activo")
  list_filter = ("activo", "marca")
  search_fields = ("nombre", "codigo")
  autocomplete_fields = ["marca"]


@admin.register(ImportacionRemitos)
class ImportacionRemitosAdmin(admin.ModelAdmin):
  list_display = ("id", "marca", "cantidad", "estado", "fecha")
  list_filter = ("estado", "marca", "fecha")
  search_fields = ("marca__nombre",)
  readonly_fields = ("fecha",)
  inlines = [ErrorImportacionInline]


@admin.register(ErrorImportacion)
class ErrorImportacionAdmin(admin.ModelAdmin):
  list_display = ("importacion", "fila", "motivo")
  list_filter = ("importacion__marca", "importacion__estado")
  search_fields = ("motivo",)


@admin.register(Remito)
class RemitoAdmin(SimpleHistoryAdmin):
  list_display = (
      "numero",
      "marca",
      "comercio",
      "estado",
      "fecha_emision",
      "fecha_pactada",
  )
  list_filter = ("estado", "marca", "fecha_emision")
  search_fields = ("numero", "comercio__razon_social", "marca__nombre")
  readonly_fields = ("fecha_creacion",)
  autocomplete_fields = ["marca", "comercio"]
  inlines = [ItemRemitoInline]
