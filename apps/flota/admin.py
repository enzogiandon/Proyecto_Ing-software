# apps/flota/admin.py
from django.contrib import admin
from .models import Vehiculo  # Importá tu modelo Vehiculo


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    # Ajustá los nombres según los campos que tenga tu modelo (ej: patente, modelo, marca)
    list_display = ("patente", "modelo", "estado")
    search_fields = ("patente", "modelo")
