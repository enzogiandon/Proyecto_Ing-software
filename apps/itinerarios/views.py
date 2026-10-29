from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.db.models import Case, IntegerField, Prefetch, Sum, Count, When
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, ListView

from apps.core.models import Transportista
from apps.remitos.models import Remito

from .forms import CrearItinerariosForm, CrearParadasForm
from .models import EstadoItinerario, EvidenciaParada, Itinerario, Parada, ProblemaParada
from .services import crear_itinerarios, crear_paradas


class ListaItinerarios(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Itinerario
    template_name = "itinerarios/itinerario_lista.html"
    context_object_name = "itinerarios"
    permission_required = "itinerarios.view_itinerario"

    def get_queryset(self):
        qs = (
            Itinerario.objects.select_related("transportista__usuario", "vehiculo")
            .prefetch_related("paradas__comercio", "paradas__remitos")
            .annotate(
                total_paradas=Count("paradas", distinct=True),
                total_remitos=Count("paradas__remitos", distinct=True),
                monto_total=Sum("paradas__remitos__total"),
            )
            .order_by("-fecha", "id")
        )

        fecha = self.request.GET.get("fecha", "").strip()
        transportista = self.request.GET.get("transportista", "").strip()
        estado = self.request.GET.get("estado", "").strip()

        if fecha:
            qs = qs.filter(fecha=fecha)
        if transportista:
            if transportista == "sin_asignar":
                qs = qs.filter(transportista__isnull=True)
            else:
                qs = qs.filter(transportista_id=transportista)
        if estado:
            qs = qs.filter(estado=estado)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["estados"] = EstadoItinerario.choices
        context["transportistas"] = Transportista.objects.select_related("usuario", "vehiculo").order_by(
            "usuario__last_name", "usuario__first_name"
        )
        context["filtro_fecha"] = self.request.GET.get("fecha", "")
        context["filtro_transportista"] = self.request.GET.get("transportista", "")
        context["filtro_estado"] = self.request.GET.get("estado", "")
        context["paradas_seguimiento"] = (
            Parada.objects.select_related("comercio", "itinerario")
            .annotate(
                prioridad_estado=Case(
                    When(estado="error", then=0),
                    default=1,
                    output_field=IntegerField(),
                )
            )
            .order_by(
                "prioridad_estado",
                "-itinerario__fecha",
                "itinerario_id",
                "orden",
                "id",
            )
        )
        return context


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
