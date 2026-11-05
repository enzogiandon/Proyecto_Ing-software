from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import (
    DetailView,
    ListView,
    UpdateView,
)

from .forms import DetallePagoFormSet, ValidarCobranzaForm
from .models import Cobranza, EstadoCobranza


class ListaCobranza(ListView):
    model = Cobranza
    template_name = "cobranza/cobranza_lista.html"
    context_object_name = "cobranzas"
    paginate_by = 25

    def get_queryset(self):
        qs = (
            super()
            .get_queryset()
            .select_related("parada__comercio")
            .order_by("-id")
        )

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


class DetalleCobranza(DetailView):
    model = Cobranza
    template_name = "cobranza/cobranza_detalle.html"
    context_object_name = "cobranza"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("parada__comercio")
            .prefetch_related("detalles", "parada__remitos")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Calculamos totales para el resumen contable
        cobranza = self.object
        detalles = cobranza.detalles.all()

        total_declarado = sum(d.monto_declarado for d in detalles)
        total_verificado = sum(
            d.monto_verificado for d in detalles if d.monto_verificado is not None
        )

        context["total_declarado"] = total_declarado
        context["total_verificado"] = total_verificado
        context["diferencia"] = total_verificado - total_declarado
        return context


class ValidarCobranza(UpdateView):
    model = Cobranza
    form_class = ValidarCobranzaForm
    template_name = "cobranza/cobranza_validar.html"
    context_object_name = "cobranza"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("parada__comercio")
            .prefetch_related("detalles", "parada__remitos")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["detalles_formset"] = DetallePagoFormSet(
                self.request.POST, instance=self.object
            )
        else:
            context["detalles_formset"] = DetallePagoFormSet(instance=self.object)

        # Emparejar formulario del formset con la instancia para acceder a monto_declarado, medio, etc.
        formset = context["detalles_formset"]
        context["detalles_con_forms"] = zip(self.object.detalles.all(), formset.forms)

        total_declarado = sum(d.monto_declarado for d in self.object.detalles.all())
        context["total_declarado"] = total_declarado
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        detalles_formset = context["detalles_formset"]

        if detalles_formset.is_valid():
            with transaction.atomic():
                self.object = form.save()
                detalles_formset.save()

            messages.success(
                self.request,
                f"Cobranza #{self.object.id} validada correctamente (Estado: {self.object.get_estado_display()}).",
            )
            return redirect(reverse("cobranza:cobranza_detalle", kwargs={"pk": self.object.pk}))
        else:
            return self.render_to_response(self.get_context_data(form=form))
