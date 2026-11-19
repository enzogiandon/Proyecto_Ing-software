from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Case, Count, IntegerField, Prefetch, Q, Sum, When
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, ListView, View

from apps.cobranza.models import AjusteCobranza, Cobranza, DetallePago
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
            .prefetch_related(
                "paradas__comercio",
                "paradas__remitos",
            )
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
                queryset=Remito.objects.select_related("marca"),
                to_attr="remitos_vigentes",
            ),
            Prefetch("evidencias", queryset=EvidenciaParada.objects.order_by("fecha")),
            Prefetch("problemas", queryset=ProblemaParada.objects.order_by("-fecha")),
        )

    def post(self, request, *args, **kwargs):
        parada = self.get_object()
        accion = request.POST.get("accion")

        if accion == "quitar_remito":
            remito_id = request.POST.get("remito_id")
            try:
                remito = parada.remitos.get(id=remito_id)
                with transaction.atomic():
                    remito.parada = None
                    remito.estado = EstadoRemito.PENDIENTE
                    remito.save(update_fields=["parada", "estado"])

                    # Si la parada no tiene más remitos vigentes, se elimina y se reordenan las paradas restantes
                    remitos_restantes = parada.remitos.exists()
                    if not remitos_restantes:
                        itinerario = parada.itinerario
                        parada_id = parada.id
                        comercio_nombre = parada.comercio.razon_social
                        AjusteCobranza.objects.filter(cobranza__parada=parada).delete()
                        DetallePago.objects.filter(cobranza__parada=parada).delete()
                        Cobranza.objects.filter(parada=parada).delete()
                        parada.delete()

                        for i, p in enumerate(
                            itinerario.paradas.all().order_by("orden", "id"), start=1
                        ):
                            p.orden = i
                            p.save(update_fields=["orden"])

                        messages.success(
                            request,
                            f"Remito #{remito.numero} desvinculado. Al no quedar remitos, la parada #{parada_id} de «{comercio_nombre}» fue eliminada del itinerario.",
                        )
                        return redirect("itinerarios:itinerario_lista")

                messages.success(
                    request,
                    f"Remito #{remito.numero} desvinculado de la parada y vuelto a estado PENDIENTE.",
                )
            except Remito.DoesNotExist:
                messages.error(
                    request, "El remito especificado no pertenece a esta parada."
                )
            return redirect("itinerarios:parada_detalle", pk=parada.pk)

        return redirect("itinerarios:parada_detalle", pk=parada.pk)


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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        itinerario_id = self.request.GET.get("itinerario")
        if itinerario_id:
            kwargs["itinerario_id"] = itinerario_id
        return kwargs

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
                            queryset=Remito.objects.select_related("marca"),
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
            remitos = getattr(p, "remitos_vigentes", list(p.remitos.all()))
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
                            queryset=Remito.objects.select_related("marca"),
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
            remitos = getattr(p, "remitos_vigentes", list(p.remitos.all()))
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

        transportistas_ocupados = (
            Itinerario.objects.filter(
                fecha=itinerario.fecha,
                transportista__isnull=False,
            )
            .exclude(pk=itinerario.pk)
            .values_list("transportista_id", flat=True)
        )
        context["transportistas"] = (
            Transportista.objects.filter(
                usuario__is_active=True,
                vehiculo__isnull=False,
            )
            .exclude(pk__in=transportistas_ocupados)
            .select_related("usuario", "vehiculo")
            .order_by("usuario__last_name", "usuario__first_name")
        )
        context["vehiculos"] = Vehiculo.objects.all().order_by("patente")
        return context

    def post(self, request, *args, **kwargs):
        itinerario = self.get_object()
        accion = request.POST.get("accion")

        if accion == "quitar_parada":
            parada_id = request.POST.get("parada_id")
            try:
                parada = itinerario.paradas.get(id=parada_id)
                comercio_nombre = parada.comercio.razon_social
                with transaction.atomic():
                    AjusteCobranza.objects.filter(cobranza__parada=parada).delete()
                    DetallePago.objects.filter(cobranza__parada=parada).delete()
                    Cobranza.objects.filter(parada=parada).delete()
                    Remito.objects.filter(parada=parada).update(
                        parada=None, estado=EstadoRemito.PENDIENTE
                    )
                    parada.delete()
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

        nueva_fecha = request.POST.get("fecha")
        transportista_id = (request.POST.get("transportista") or "").strip()
        vehiculo_id = (request.POST.get("vehiculo") or "").strip()

        if nueva_fecha:
            itinerario.fecha = nueva_fecha

        if transportista_id:
            try:
                t = Transportista.objects.select_related("usuario", "vehiculo").get(
                    pk=transportista_id,
                    usuario__is_active=True,
                    vehiculo__isnull=False,
                )
            except Transportista.DoesNotExist:
                messages.error(request, "Transportista no asignado")
                return redirect("itinerarios:itinerario_editar", pk=itinerario.pk)

            ocupado = (
                Itinerario.objects.filter(
                    fecha=itinerario.fecha,
                    transportista=t,
                )
                .exclude(pk=itinerario.pk)
                .exists()
            )
            if ocupado:
                messages.error(request, "Transportista no asignado")
                return redirect("itinerarios:itinerario_editar", pk=itinerario.pk)

            itinerario.transportista = t
            if vehiculo_id:
                try:
                    itinerario.vehiculo = Vehiculo.objects.get(pk=vehiculo_id)
                except Vehiculo.DoesNotExist:
                    itinerario.vehiculo = t.vehiculo
            else:
                itinerario.vehiculo = t.vehiculo

            if itinerario.estado == EstadoItinerario.PENDIENTE:
                itinerario.estado = EstadoItinerario.ASIGNADO
        else:
            itinerario.transportista = None
            if vehiculo_id:
                try:
                    itinerario.vehiculo = Vehiculo.objects.get(pk=vehiculo_id)
                except Vehiculo.DoesNotExist:
                    itinerario.vehiculo = None
            else:
                itinerario.vehiculo = None

            if itinerario.estado == EstadoItinerario.ASIGNADO:
                itinerario.estado = EstadoItinerario.PENDIENTE

        itinerario.save()
        messages.success(request, "Transportista asignado con éxito")
        return redirect("itinerarios:itinerario_lista")


class EliminarItinerario(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "itinerarios.delete_itinerario"

    def post(self, request, pk, *args, **kwargs):
        itinerario = Itinerario.objects.filter(pk=pk).first()
        if not itinerario:
            messages.error(request, "Itinerario no encontrado")
            return redirect("itinerarios:itinerario_lista")

        if itinerario.estado == EstadoItinerario.FINALIZADO:
            messages.error(
                request, "No se puede eliminar un itinerario finalizado."
            )
            return redirect("itinerarios:itinerario_lista")

        with transaction.atomic():
            AjusteCobranza.objects.filter(
                cobranza__parada__itinerario=itinerario
            ).delete()
            DetallePago.objects.filter(
                cobranza__parada__itinerario=itinerario
            ).delete()
            Cobranza.objects.filter(parada__itinerario=itinerario).delete()
            Remito.objects.filter(parada__itinerario=itinerario).update(
                parada=None,
                estado=EstadoRemito.PENDIENTE,
            )
            itinerario.delete()

        messages.success(request, "Itinerario eliminado exitosamente")
        return redirect("itinerarios:itinerario_lista")

    def get(self, request, pk, *args, **kwargs):
        return redirect("itinerarios:itinerario_lista")
