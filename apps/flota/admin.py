# apps/flota/admin.py
from django.contrib import admin

from .models import Vehiculo  # Importá tu modelo Vehiculo


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ("patente", "modelo", "estado")
    search_fields = ("patente", "modelo")
