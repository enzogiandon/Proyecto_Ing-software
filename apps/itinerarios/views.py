from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.db.models import Prefetch
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, ListView

from apps.remitos.models import Remito

from .forms import CrearItinerariosForm, CrearParadasForm
from .models import EvidenciaParada, Itinerario, Parada, ProblemaParada
from .services import crear_itinerarios, crear_paradas


class ListaItinerarios(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Itinerario
    template_name = "itinerarios/itinerario_lista.html"
    context_object_name = "itinerarios"
    permission_required = "itinerarios.view_itinerario"

    def get_queryset(self):
        return (
            Itinerario.objects.select_related("transportista__usuario", "vehiculo")
            .prefetch_related("paradas__comercio")
            .order_by("-fecha", "id")
        )


class DetalleParada(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Parada
    template_name = "itinerarios/parada_detalle.html"
    context_object_name = "parada"
    permission_required = "itinerarios.view_parada"

    def get_queryset(self):
        return (
            Parada.objects.select_related(
                "comercio",
                "itinerario__transportista__usuario",
                "itinerario__vehiculo",
            )
            .prefetch_related(
                Prefetch(
                    "remitos",
                    queryset=Remito.objects.filter(eliminado=False).select_related(
                        "marca"
                    ),
                    to_attr="remitos_vigentes",
                ),
                Prefetch("evidencias", queryset=EvidenciaParada.objects.order_by("fecha")),
                Prefetch("problemas", queryset=ProblemaParada.objects.order_by("-fecha")),
            )
        )


class CrearItinerarios(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, FormView
):
    form_class = CrearItinerariosForm
    template_name = "itinerarios/itinerario_form.html"
    success_url = reverse_lazy("itinerarios:itinerario_lista")
    success_message = "Itinerario guardado correctamente"
    permission_required = "itinerarios.add_itinerario"

    def form_valid(self, form):
        try:
            crear_itinerarios(
                form.cleaned_data["transportistas"],
                form.cleaned_data["fecha"],
            )
        except ValidationError as error:
            form.add_error(None, error)
            return self.form_invalid(form)
        return super().form_valid(form)


class CrearParadas(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, FormView
):
    form_class = CrearParadasForm
    template_name = "itinerarios/paradas_form.html"
    success_url = reverse_lazy("itinerarios:itinerario_lista")
    success_message = "Paradas asignadas correctamente"
    permission_required = ("itinerarios.add_parada", "remitos.change_remito")

    def form_valid(self, form):
        try:
            crear_paradas(
                form.cleaned_data["itinerario"],
                form.cleaned_data["comercios"],
            )
        except ValidationError as error:
            form.add_error(None, error)
            return self.form_invalid(form)
        return super().form_valid(form)
