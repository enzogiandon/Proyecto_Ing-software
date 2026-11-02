from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import (
    Comercio,
    ErrorImportacion,
    ImportacionRemitos,
    Marca,
    Remito,
)

# ---------------------------------------------------------
# Inlines: para ver/cargar elementos relacionados adentro del padre
# ---------------------------------------------------------


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
        "total",
    )
    list_filter = ("estado", "marca" )
    search_fields = ("numero", "comercio__razon_social", "marca__nombre")
    autocomplete_fields = ["marca", "comercio"]

