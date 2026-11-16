
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
)

from apps.remitos.models import Remito

from .forms import (
    AjusteCobranzaForm,
    DetallePagoFormSet,
    ValidarCobranzaForm,
)
from .models import AjusteCobranza, Cobranza, EstadoCobranza


class ListaCobranza(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Cobranza
    template_name = "cobranza/cobranza_lista.html"
    context_object_name = "cobranzas"
    paginate_by = 25
    permission_required = "cobranza.view_cobranza"

    def get_queryset(self):
        qs = super().get_queryset().select_related("parada__comercio").order_by("-id")

        comercio = self.request.GET.get("comercio", "").strip()
        estado = self.request.GET.get("estado", "").strip()
        fecha = self.request.GET.get("fecha", "").strip()

        if comercio:
            qs = qs.filter(parada__comercio__razon_social__icontains=comercio)
        if estado:
            qs = qs.filter(estado=estado)
        if fecha:
            qs = qs.filter(fecha__date=fecha)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Opciones para los desplegables
        context["estados"] = EstadoCobranza.choices

        # Variables para mantener el estado del formulario en el HTML
        context["filtro_comercio"] = self.request.GET.get("comercio", "")
        context["filtro_estado"] = self.request.GET.get("estado", "")
        context["filtro_fecha"] = self.request.GET.get("fecha", "")
        return context


class DetalleCobranza(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Cobranza
    template_name = "cobranza/cobranza_detalle.html"
    context_object_name = "cobranza"
    permission_required = "cobranza.view_cobranza"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("parada__comercio")
            .prefetch_related(
                "detalles",
                "ajustes__usuario",
                Prefetch(
                    "parada__remitos",
                    queryset=Remito.objects.filter(eliminado=False),
                ),
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Calculamos totales para el resumen contable
        cobranza = self.object
        detalles = cobranza.detalles.all()
        ajustes = cobranza.ajustes.all()

        total_declarado = sum(d.monto_declarado for d in detalles)
        total_verificado = sum(
            d.monto_verificado for d in detalles if d.monto_verificado is not None
        )
        total_ajustes = sum(a.monto for a in ajustes)
        total_ajustado = total_verificado + total_ajustes

        context["total_declarado"] = total_declarado
        context["total_verificado"] = total_verificado
        context["total_ajustes"] = total_ajustes
        context["total_ajustado"] = total_ajustado
        context["diferencia"] = total_ajustado - total_declarado
        return context


class ValidarCobranza(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Cobranza
    form_class = ValidarCobranzaForm
    template_name = "cobranza/cobranza_validar.html"
    context_object_name = "cobranza"
    permission_required = ("cobranza.change_cobranza", "cobranza.change_detallepago")

    def dispatch(self, request, *args, **kwargs):
        cobranza = self.get_object()
        if cobranza.estado != EstadoCobranza.REGISTRADO:
            messages.warning(
                request,
                f"La Cobranza #{cobranza.id} ya se encuentra validada y no puede ser modificada directamente.",
            )
            return redirect("cobranza:cobranza_detalle", pk=cobranza.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("parada__comercio")
            .prefetch_related("detalles")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["detalles_formset"] = DetallePagoFormSet(
                self.request.POST, instance=self.object
            )
        else:
            context["detalles_formset"] = DetallePagoFormSet(instance=self.object)

        formset = context["detalles_formset"]
        context["detalles_con_forms"] = zip(self.object.detalles.all(), formset.forms)
        context["total_declarado"] = sum(
            d.monto_declarado for d in self.object.detalles.all()
        )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        detalles_formset = context["detalles_formset"]

        if not detalles_formset.is_valid():
            return self.render_to_response(self.get_context_data(form=form))

        nuevo_estado = detalles_formset.estado_calculado
        observacion = form.cleaned_data.get("observacion", "").strip()

        if (
            nuevo_estado == EstadoCobranza.DIFIERE
            and not observacion
        ):
            form.add_error(
                "observacion",
                f"El estado resultante es '{nuevo_estado.label}'. Es obligatorio ingresar una justificación.",
            )
            return self.render_to_response(self.get_context_data(form=form))

        with transaction.atomic():
            cobranza = form.save(commit=False)
            cobranza.estado = nuevo_estado  # 👈 Asignación automática del estado
            cobranza.save()
            detalles_formset.save()

        messages.success(
            self.request,
            f"Cobranza #{cobranza.id} validada. Estado asignado: {cobranza.get_estado_display()}.",
        )
        return redirect(
            reverse("cobranza:cobranza_detalle", kwargs={"pk": cobranza.pk})
        )


class AjustarCobranza(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView
):
    model = AjusteCobranza
    form_class = AjusteCobranzaForm
    template_name = "cobranza/cobranza_ajustar.html"
    success_message = "Ajuste registrado correctamente en la cobranza."
    permission_required = "cobranza.add_ajustecobranza"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.cobranza = get_object_or_404(
            Cobranza.objects.select_related("parada__comercio").prefetch_related("detalles", "ajustes"),
            pk=self.kwargs["pk"],
        )

    def dispatch(self, request, *args, **kwargs):
        if self.cobranza.estado in [EstadoCobranza.REGISTRADO]:
            messages.warning(
                request,
                f"La cobranza #{self.cobranza.id} no puede ajustarse en estado '{self.cobranza.get_estado_display()}'.",
            )
            return redirect("cobranza:cobranza_detalle", pk=self.cobranza.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cobranza"] = self.cobranza
        return context

    def form_valid(self, form):
        form.instance.cobranza = self.cobranza
        form.instance.usuario = self.request.user
        with transaction.atomic():
            response = super().form_valid(form)
            self.cobranza.actualizar_tras_ajuste()
        return response

    def get_success_url(self):
        return reverse("cobranza:cobranza_detalle", kwargs={"pk": self.cobranza.pk})


class ListaAjustesCobranza(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = AjusteCobranza
    template_name = "cobranza/ajuste_lista.html"
    context_object_name = "ajustes"
    paginate_by = 25
    permission_required = "cobranza.view_ajustecobranza"

    def get_queryset(self):
        qs = (
            super()
            .get_queryset()
            .select_related(
                "usuario",
                "cobranza__parada__comercio",
            )
            .order_by("-fecha", "-id")
        )

        comercio = self.request.GET.get("comercio", "").strip()
        fecha = self.request.GET.get("fecha", "").strip()

        if comercio:
            qs = qs.filter(
                cobranza__parada__comercio__razon_social__icontains=comercio
            )
        if fecha:
            qs = qs.filter(fecha__date=fecha)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filtro_comercio"] = self.request.GET.get("comercio", "")
        context["filtro_fecha"] = self.request.GET.get("fecha", "")
        return context
