from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, ListView, TemplateView, UpdateView
from apps.remitos.models import (
    Remito,
    ImportacionRemitos,
    EstadoImportacion,
    EstadoRemito,
)
from apps.itinerarios.models import Parada, EstadoParada, EstadoItinerario, Itinerario
from apps.cobranza.models import Cobranza, DetallePago, EstadoCobranza

from .forms import EmpleadoCreateForm, EmpleadoUpdateForm, LoginForm, VehiculoForm
from .models import EstadoVehiculo, Usuario, Vehiculo

# Create your views here.


class CustomLoginView(LoginView):
    template_name = "core/login.html"
    form_class = LoginForm

    # redirect_authenticated_user = True
    def form_valid(self, form):
        user = form.get_user()
        user.last_login = timezone.now()
        user.intentos_fallidos = 0
        user.save(update_fields=["last_login", "intentos_fallidos"])
        return super().form_valid(form)

    def form_invalid(self, form):
        username = form.cleaned_data.get("username")

        try:
            user = Usuario.objects.get(username=username)
            if user.is_active:
                user.intentos_fallidos += 1
                if user.intentos_fallidos >= 5:
                    user.is_active = False
            else:
                form.add_error(
                    None,
                    "La cuenta se encuentra suspendida. Contacte al administrador.",
                )

            user.save(update_fields=["intentos_fallidos", "is_active"])

        except ObjectDoesNotExist:
            pass
        return super().form_invalid(form)


class ListaVehiculos(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Vehiculo
    template_name = "core/vehiculo_lista.html"
    context_object_name = "vehiculos"
    permission_required = "core.view_vehiculo"

    def get_queryset(self):
        return Vehiculo.objects.order_by("patente")


class CrearVehiculo(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView
):
    model = Vehiculo
    form_class = VehiculoForm
    template_name = "core/vehiculo_form.html"
    success_url = reverse_lazy("core:vehiculo_lista")
    success_message = "Vehículo registrado exitosamente"
    permission_required = "core.add_vehiculo"

    def form_invalid(self, form):
        if "Vehículo repetido" in form.errors.get("patente", []):
            messages.error(self.request, "Vehículo repetido")
            return redirect(self.success_url)
        return super().form_invalid(form)


class EditarVehiculo(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView
):
    model = Vehiculo
    form_class = VehiculoForm
    template_name = "core/vehiculo_form.html"
    context_object_name = "vehiculo"
    success_url = reverse_lazy("core:vehiculo_lista")
    success_message = "Vehículo modificado exitosamente"
    permission_required = "core.change_vehiculo"


class ListaEmpleados(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Usuario
    template_name = "core/empleado_lista.html"
    context_object_name = "empleados"
    permission_required = "core.view_usuario"

    def get_queryset(self):
        return Usuario.objects.order_by("last_name", "first_name", "id")


class CrearEmpleado(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView
):
    form_class = EmpleadoCreateForm
    template_name = "core/empleado_form.html"
    success_url = reverse_lazy("core:empleado_lista")
    success_message = "Empleado registrado correctamente"
    permission_required = "core.add_usuario"


class EditarEmpleado(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView
):
    model = Usuario
    form_class = EmpleadoUpdateForm
    template_name = "core/empleado_form.html"
    context_object_name = "empleado"
    success_url = reverse_lazy("core:empleado_lista")
    success_message = "Empleado modificado correctamente"
    permission_required = "core.change_usuario"


class SuspenderEmpleado(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "core.change_usuario"

    def post(self, request, pk):
        empleado = get_object_or_404(Usuario, pk=pk)
        if empleado and empleado.is_active:
            empleado.is_active = False
            empleado.save(update_fields=["is_active"])
            messages.success(request, "Cuenta del empleado deshabilitada.")
        else:
            empleado.is_active = True
            empleado.save(update_fields=["is_active"])
            messages.success(request, "Cuenta del empleado habilitada.")

        return redirect("core:empleado_lista")


class Inicio(LoginRequiredMixin, TemplateView):
    template_name = "core/inicio.html"
    login_url = reverse_lazy("core:login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["username"] = user.first_name or user.username

        # --------------------------------------------------
        # Administración de Personal
        # --------------------------------------------------
        context["empleados_activos"] = Usuario.objects.filter(is_active=True).count()

        # Agregamos ambos estados de vehículos en una sola query a la DB
        vehiculos_stats = Vehiculo.objects.aggregate(
            disponibles=Count("id", filter=Q(estado=EstadoVehiculo.DISPONIBLE)),
            no_disponibles=Count("id", filter=Q(estado=EstadoVehiculo.ASIGNADO)),
        )
        context["vehiculos_disponibles"] = vehiculos_stats["disponibles"]
        context["vehiculos_asignados"] = vehiculos_stats["no_disponibles"]

        # --------------------------------------------------
        # Planificación
        # --------------------------------------------------
        context["remitos_asignados"] = Remito.objects.filter(
            estado=EstadoRemito.ASIGNADO
        ).count()
        context["itinerarios_asignados"] = Itinerario.objects.filter(
            estado=EstadoItinerario.ASIGNADO
        ).count()
        context["importaciones_pendientes"] = ImportacionRemitos.objects.filter(
            estado=EstadoImportacion.PENDIENTE
        ).count()

        # --------------------------------------------------
        # Conciliación
        # --------------------------------------------------
        context["cobranzas_para_validar"] = Cobranza.objects.filter(
            estado=EstadoCobranza.REGISTRADO
        ).count()

        # Mismo caso: pagos con diferencia y no encontrados en una sola query
        pagos_stats = Cobranza.objects.aggregate(
            para_validar=Count("id", filter=Q(estado=EstadoCobranza.REGISTRADO)),
            con_diferencia=Count("id", filter=Q(estado=EstadoCobranza.DIFIERE)),
            no_encontrados=Count("id", filter=Q(estado=EstadoCobranza.NO_ENCONTRADO)),
        )
        context["cobranzas_para_validar"] = pagos_stats["para_validar"]
        context["cobranza_con_diferencia"] = pagos_stats["con_diferencia"]
        context["cobranza_no_encontrados"] = pagos_stats["no_encontrados"]

        context["ultimos_empleados"] = (
            Usuario.objects.filter(is_active=True)
            .prefetch_related("groups")
            .order_by("-date_joined")[:3]
        )
        context["cobranzas_pendientes"] = (
            Cobranza.objects.filter(estado=EstadoCobranza.REGISTRADO)
            .order_by("-id")[:3]
        )
        context["importaciones"] = ImportacionRemitos.objects.all().order_by("-id")[:3]

        return context


def error_404(request, exception):
    return render(request, "errores/404.html", status=404)


def error_500(request):
    return render(request, "errores/500.html", status=500)


def error_403(request, exception):
    return render(request, "errores/403.html", status=403)
