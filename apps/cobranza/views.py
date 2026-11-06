from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
    UpdateView,
    View,
)

from .forms import (
    AjusteItemForm,
    AjusteItemFormSet,
    DetallePagoFormSet,
    ValidarCobranzaForm,
)
from .models import AjusteCobranza, Cobranza, DetallePago, EstadoCobranza


class ListaCobranza(ListView):
    model = Cobranza
    template_name = "cobranza/cobranza_lista.html"
    context_object_name = "cobranzas"
    paginate_by = 25

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

    def dispatch(self, request, *args, **kwargs):
        cobranza = self.get_object()
        # Si ya fue aprobada, no se puede volver a validar directamente
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

        # Validamos ambos formularios
        if not detalles_formset.is_valid():
            return self.render_to_response(self.get_context_data(form=form))

        nuevo_estado = detalles_formset.estado_calculado
        observacion = form.cleaned_data.get("observacion_ajuste", "").strip()

        # Validación cruzada: si no se aprueba, obligamos a escribir observación
        if (
            nuevo_estado in [EstadoCobranza.DIFIERE, EstadoCobranza.NO_ENCONTRADO]
            and not observacion
        ):
            form.add_error(
                "observacion_ajuste",
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


class AjustarCobranza(LoginRequiredMixin, View):
    template_name = "cobranza/cobranza_ajustar.html"

    def dispatch(self, request, *args, **kwargs):
        self.cobranza = get_object_or_404(
            Cobranza.objects.select_related("parada__comercio").prefetch_related("detalles"),
            pk=self.kwargs["pk"],
        )

        if self.cobranza.estado not in [EstadoCobranza.REGISTRADO, EstadoCobranza.DIFIERE]:
            messages.warning(
                request,
                f"La cobranza #{self.cobranza.id} no puede ajustarse en estado '{self.cobranza.get_estado_display()}'.",
            )
            return redirect("cobranza:cobranza_detalle", pk=self.cobranza.pk)

        return super().dispatch(request, *args, **kwargs)

    def get_detalles_discrepantes(self):
        """Retorna solo los detalles donde el verificado no coincide con el declarado o es nulo."""
        discrepantes = []
        for det in self.cobranza.detalles.all():
            monto_verif = det.monto_verificado
            if monto_verif is None or monto_verif != det.monto_declarado:
                discrepantes.append(det)
        return discrepantes

    def get(self, request, *args, **kwargs):
        detalles_a_ajustar = self.get_detalles_discrepantes()

        if not detalles_a_ajustar:
            messages.info(request, "No hay detalles de pago con diferencias para ajustar.")
            return redirect("cobranza:cobranza_detalle", pk=self.cobranza.pk)

        initial_data = [
            {
                "detalle_id": det.id,
                "importe_nuevo": det.monto_verificado if det.monto_verificado is not None else det.monto_declarado,
                "motivo": "",
            }
            for det in detalles_a_ajustar
        ]
        formset = AjusteItemFormSet(initial=initial_data)

        detalles_forms = list(zip(detalles_a_ajustar, formset.forms))

        return render(
            request,
            self.template_name,
            {
                "cobranza": self.cobranza,
                "formset": formset,
                "detalles_forms": detalles_forms,
            },
        )

    def post(self, request, *args, **kwargs):
        detalles_a_ajustar = self.get_detalles_discrepantes()
        formset = AjusteItemFormSet(request.POST)

        if not formset.is_valid():
            detalles_forms = list(zip(detalles_a_ajustar, formset.forms))
            return render(
                request,
                self.template_name,
                {
                    "cobranza": self.cobranza,
                    "formset": formset,
                    "detalles_forms": detalles_forms,
                },
            )

        detalles_map = {d.id: d for d in detalles_a_ajustar}
        ajustes_a_crear = []
        detalles_a_guardar = []
        motivos_registrados = []

        with transaction.atomic():
            for form in formset.forms:
                det_id = form.cleaned_data["detalle_id"]
                nuevo_importe = form.cleaned_data["importe_nuevo"]
                motivo = form.cleaned_data["motivo"]

                detalle = detalles_map.get(det_id)
                if not detalle:
                    continue

                importe_anterior = (
                    detalle.monto_verificado
                    if detalle.monto_verificado is not None
                    else detalle.monto_declarado
                )

                ajustes_a_crear.append(
                    AjusteCobranza(
                        detalle_pago=detalle,
                        usuario=request.user,
                        importe_anterior=importe_anterior,
                        importe_nuevo=nuevo_importe,
                        motivo=motivo,
                    )
                )
                detalle.monto_verificado = nuevo_importe
                detalles_a_guardar.append(detalle)
                motivos_registrados.append(f"{detalle.get_medio_display()}: {motivo}")

            AjusteCobranza.objects.bulk_create(ajustes_a_crear)
            DetallePago.objects.bulk_update(detalles_a_guardar, fields=["monto_verificado"])

            detalles_actualizados = self.cobranza.detalles.all()
            total_declarado = sum(d.monto_declarado for d in detalles_actualizados)
            total_verificado = sum(
                d.monto_verificado for d in detalles_actualizados if d.monto_verificado is not None
            )

            if total_declarado == total_verificado and all(
                d.monto_verificado is not None for d in detalles_actualizados
            ):
                self.cobranza.estado = EstadoCobranza.APROBADO
            else:
                self.cobranza.estado = EstadoCobranza.DIFIERE

            motivos_str = " | ".join(motivos_registrados)
            self.cobranza.observacion_ajuste = (
                f"[Ajustado por {request.user.username}]: {motivos_str}"
            )
            self.cobranza.save(update_fields=["estado", "observacion_ajuste"])

        messages.success(
            request,
            f"Se aplicaron {len(ajustes_a_crear)} ajuste(s) correctamente a la Cobranza #{self.cobranza.id}.",
        )
        return redirect("cobranza:cobranza_detalle", pk=self.cobranza.pk)


class ListaAjustesCobranza(LoginRequiredMixin, ListView):
    model = AjusteCobranza
    template_name = "cobranza/ajuste_lista.html"
    context_object_name = "ajustes"
    paginate_by = 25

    def get_queryset(self):
        qs = (
            super()
            .get_queryset()
            .select_related(
                "usuario",
                "detalle_pago__cobranza__parada__comercio",
            )
            .order_by("-fecha", "-id")
        )

        comercio = self.request.GET.get("comercio", "").strip()
        fecha = self.request.GET.get("fecha", "").strip()

        if comercio:
            qs = qs.filter(
                detalle_pago__cobranza__parada__comercio__razon_social__icontains=comercio
            )
        if fecha:
            qs = qs.filter(fecha__date=fecha)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filtro_comercio"] = self.request.GET.get("comercio", "")
        context["filtro_fecha"] = self.request.GET.get("fecha", "")
        return context
