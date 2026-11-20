# itinerarios/admin.py

from django.contrib import admin
from .models import DetalleRutaGuardada, Itinerario, Parada, RutaGuardada


# -------------------------------------------------------------------
# Inlines
# -------------------------------------------------------------------
class ParadaInline(admin.TabularInline):
  model = Parada
  extra = 1
  ordering = ("orden",)
  autocomplete_fields = ["comercio"]
  fields = ("orden", "comercio", "estado")


class DetalleRutaGuardadaInline(admin.TabularInline):
  model = DetalleRutaGuardada
  extra = 1
  ordering = ("-prioridad",)
  autocomplete_fields = ["comercio"]
  fields = ("prioridad", "comercio")


# -------------------------------------------------------------------
# ModelAdmins
# -------------------------------------------------------------------
@admin.register(Itinerario)
class ItinerarioAdmin(admin.ModelAdmin):
  list_display = ("id", "fecha", "estado", "transportista", "vehiculo")
  list_filter = ("estado", "fecha")
  search_fields = (
      "id",
      "transportista__username",
      "transportista__first_name",
      "transportista__last_name",
  )
  date_hierarchy = "fecha"
  autocomplete_fields = ["transportista", "vehiculo"]
  inlines = [ParadaInline]


@admin.register(Parada)
class ParadaAdmin(admin.ModelAdmin):
  list_display = ("id", "itinerario", "comercio", "orden", "estado")
  list_filter = ("estado", "itinerario__fecha")
  search_fields = ("comercio__razon_social", "itinerario__id")
  autocomplete_fields = ["itinerario", "comercio"]


@admin.register(RutaGuardada)
class RutaGuardadaAdmin(admin.ModelAdmin):
  list_display = ("nombre", "transportista")
  search_fields = ("nombre", "transportista__usuario__username")
  autocomplete_fields = ["transportista"]
  inlines = [DetalleRutaGuardadaInline]


@admin.register(DetalleRutaGuardada)
class DetalleRutaGuardadaAdmin(admin.ModelAdmin):
  list_display = ("ruta_guardada", "comercio", "prioridad")
  list_filter = ("prioridad",)
  search_fields = ("ruta_guardada__nombre", "comercio__razon_social")
  autocomplete_fields = ["ruta_guardada", "comercio"]
