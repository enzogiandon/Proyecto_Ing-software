from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Transportista, Usuario, Vehiculo


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "telefono",
        "intentos_fallidos",
        "is_staff",
        "is_active",
    )

    # Filtros laterales
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")

    search_fields = ("username", "email", "first_name", "last_name")
    readonly_fields = ("last_login", "date_joined", "intentos_fallidos")
    ordering = ("username",)

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Información personal",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "telefono",
                    "email",
                    "intentos_fallidos",
                )
            },
        ),
        (
            "Permisos",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Fechas importantes", {"fields": ("last_login", "date_joined")}),
    )

@admin.register(Transportista)
class TransportistaAdmin(admin.ModelAdmin):
  list_display = ("usuario",  "vehiculo")
  search_fields = (
      "usuario__username",
      "usuario__first_name",
      "usuario__last_name",
  )

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ("patente", "modelo", "estado")
    search_fields = ("patente", "modelo")

