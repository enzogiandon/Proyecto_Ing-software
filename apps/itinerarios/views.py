from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Case, Count, IntegerField, Prefetch, Sum, When
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, ListView

from apps.core.models import Transportista, Vehiculo
from apps.remitos.models import EstadoRemito, Remito

from .forms import CrearItinerariosForm, CrearParadasForm
from .models import (
    EstadoItinerario,
    EvidenciaParada,
    Itinerario,
    Parada,
    ProblemaParada,
)
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
        context["transportistas"] = Transportista.objects.select_related(
            "usuario", "vehiculo"
        ).order_by("usuario__last_name", "usuario__first_name")
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
        return Parada.objects.select_related(
            "comercio",
            "itinerario__transportista__usuario",
            "itinerario__vehiculo",
        ).prefetch_related(
            Prefetch(
                "remitos",
                queryset=Remito.objects.filter(eliminado=False).select_related("marca"),
                to_attr="remitos_vigentes",
            ),
            Prefetch("evidencias", queryset=EvidenciaParada.objects.order_by("fecha")),
            Prefetch("problemas", queryset=ProblemaParada.objects.order_by("-fecha")),
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


class ReordenarItinerario(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Itinerario
    template_name = "itinerarios/itinerario_reordenar.html"
    context_object_name = "itinerario"
    permission_required = "itinerarios.change_parada"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("transportista__usuario", "vehiculo")
            .prefetch_related(
                Prefetch(
                    "paradas",
                    queryset=Parada.objects.select_related("comercio")
                    .prefetch_related(
                        Prefetch(
                            "remitos",
                            queryset=Remito.objects.filter(eliminado=False).select_related("marca"),
                            to_attr="remitos_vigentes",
                        )
                    )
                    .order_by("orden", "id"),
                )
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        itinerario = self.object
        paradas = list(itinerario.paradas.all())

        total_remitos = 0
        total_productos = 0
        total_monto = 0

        for p in paradas:
            remitos = getattr(p, "remitos_vigentes", list(p.remitos.filter(eliminado=False)))
            p.remitos_asociados = remitos
            p.monto_total = sum(r.total for r in remitos)
            p.total_remitos_count = len(remitos)
            p.total_productos_count = len(remitos) * 10 if remitos else 0
            total_remitos += p.total_remitos_count
            total_productos += p.total_productos_count
            total_monto += p.monto_total

        context["paradas_lista"] = paradas
        context["total_remitos"] = total_remitos
        context["total_productos"] = total_productos
        context["total_monto"] = total_monto
        return context

    def post(self, request, *args, **kwargs):
        itinerario = self.get_object()
        parada_ids = request.POST.getlist("paradas_ordenadas")

        if not parada_ids:
            messages.error(request, "No se recibieron paradas para reordenar.")
            return redirect("itinerarios:itinerario_reordenar", pk=itinerario.pk)

        paradas_actuales = {p.id: p for p in itinerario.paradas.all().order_by("orden")}

        try:
            ids_enteros = [int(p_id) for p_id in parada_ids]
        except ValueError:
            messages.error(request, "Los identificadores de paradas son inválidos.")
            return redirect("itinerarios:itinerario_reordenar", pk=itinerario.pk)

        if set(ids_enteros) != set(paradas_actuales.keys()):
            messages.error(
                request, "La lista no coincide con las paradas de este itinerario."
            )
            return redirect("itinerarios:itinerario_reordenar", pk=itinerario.pk)

        paradas_a_guardar = []
        for nuevo_orden, p_id in enumerate(ids_enteros, start=1):
            parada = paradas_actuales[p_id]
            parada.orden = nuevo_orden
            paradas_a_guardar.append(parada)

        with transaction.atomic():
            Parada.objects.bulk_update(paradas_a_guardar, fields=["orden"])

        messages.success(
            request, f"Recorrido del Itinerario #{itinerario.id} reordenado con éxito."
        )
        return redirect("itinerarios:itinerario_lista")


class EditarItinerario(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Itinerario
    template_name = "itinerarios/itinerario_editar.html"
    context_object_name = "itinerario"
    permission_required = "itinerarios.change_itinerario"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("transportista__usuario", "vehiculo")
            .prefetch_related(
                Prefetch(
                    "paradas",
                    queryset=Parada.objects.select_related("comercio")
                    .prefetch_related(
                        Prefetch(
                            "remitos",
                            queryset=Remito.objects.filter(eliminado=False).select_related("marca"),
                            to_attr="remitos_vigentes",
                        )
                    )
                    .order_by("orden", "id"),
                )
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        itinerario = self.object
        paradas = list(itinerario.paradas.all())

        total_remitos = 0
        total_productos = 0
        total_monto = 0

        for p in paradas:
            remitos = getattr(p, "remitos_vigentes", list(p.remitos.filter(eliminado=False)))
            p.remitos_asociados = remitos
            p.monto_total = sum(r.total for r in remitos)
            p.total_remitos_count = len(remitos)
            p.total_productos_count = len(remitos) * 10 if remitos else 0
            total_remitos += p.total_remitos_count
            total_productos += p.total_productos_count
            total_monto += p.monto_total

        context["paradas_lista"] = paradas
        context["total_remitos"] = total_remitos
        context["total_productos"] = total_productos
        context["total_monto"] = total_monto

        context["transportistas"] = (
            Transportista.objects.filter(
                usuario__is_active=True,
                vehiculo__isnull=False,
            )
            .select_related("usuario", "vehiculo")
            .order_by("usuario__last_name", "usuario__first_name")
        )
        context["vehiculos"] = Vehiculo.objects.all().order_by("patente")
        return context

    def post(self, request, *args, **kwargs):
        itinerario = self.get_object()
        accion = request.POST.get("accion")

        # Quitar parada individual
        if accion == "quitar_parada":
            parada_id = request.POST.get("parada_id")
            try:
                parada = itinerario.paradas.get(id=parada_id)
                comercio_nombre = parada.comercio.razon_social
                with transaction.atomic():
                    # Desvincular remitos y devolverlos a PENDIENTE
                    Remito.objects.filter(parada=parada).update(
                        parada=None, estado=EstadoRemito.PENDIENTE
                    )
                    parada.delete()
                    # Reordenar las paradas restantes
                    for idx, p in enumerate(
                        itinerario.paradas.all().order_by("orden", "id"), start=1
                    ):
                        p.orden = idx
                        p.save(update_fields=["orden"])

                messages.success(
                    request,
                    f"Parada de «{comercio_nombre}» quitada del itinerario.",
                )
            except Parada.DoesNotExist:
                messages.error(
                    request, "La parada especificada no existe en este itinerario."
                )
            return redirect("itinerarios:itinerario_editar", pk=itinerario.pk)

        # Guardar cambios generales (Fecha, Transportista, Vehículo)
        nueva_fecha = request.POST.get("fecha")
        transportista_id = request.POST.get("transportista")
        vehiculo_id = request.POST.get("vehiculo")

        if nueva_fecha:
            itinerario.fecha = nueva_fecha

        if transportista_id:
            try:
                t = Transportista.objects.select_related("vehiculo").get(pk=transportista_id)
                itinerario.transportista = t
                if not vehiculo_id and t.vehiculo:
                    itinerario.vehiculo = t.vehiculo
            except Transportista.DoesNotExist:
                pass

        if vehiculo_id:
            try:
                itinerario.vehiculo = Vehiculo.objects.get(pk=vehiculo_id)
            except Vehiculo.DoesNotExist:
                pass

        itinerario.save()
        messages.success(request, f"Itinerario #{itinerario.id} actualizado con éxito.")
        return redirect("itinerarios:itinerario_lista")
