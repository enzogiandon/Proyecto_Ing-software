from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from .forms import VehiculoForm
from .models import Vehiculo


class ListaVehiculos(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Vehiculo
    template_name = "flota/vehiculo_lista.html"
    context_object_name = "vehiculos"
    permission_required = "flota.view_vehiculo"

    def get_queryset(self):
        return Vehiculo.objects.order_by("patente")


class CrearVehiculo(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView
):
    model = Vehiculo
    form_class = VehiculoForm
    template_name = "flota/vehiculo_form.html"
    success_url = reverse_lazy("flota:vehiculo_lista")
    success_message = "Vehículo registrado exitosamente"
    permission_required = "flota.add_vehiculo"

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
    template_name = "flota/vehiculo_form.html"
    context_object_name = "vehiculo"
    success_url = reverse_lazy("flota:vehiculo_lista")
    success_message = "Vehículo modificado exitosamente"
    permission_required = "flota.change_vehiculo"
