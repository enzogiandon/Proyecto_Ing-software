from decimal import Decimal
from io import BytesIO
from xml.sax.saxutils import escape

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.db import DatabaseError, transaction
from django.db.models import (
    Case,
    Count,
    IntegerField,
    Prefetch,
    ProtectedError,
    Q,
    Sum,
    When,
)
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, ListView, View
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from apps.cobranza.models import Cobranza
from apps.core.models import Transportista, Vehiculo
from apps.remitos.models import EstadoRemito, Remito

from .forms import CrearItinerariosForm, CrearParadasForm
from .models import (
    EstadoItinerario,
    EstadoParada,
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


class ExportarHojaRutaPDF(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Itinerario
    permission_required = "itinerarios.view_itinerario"

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
                            queryset=Remito.objects.order_by("numero"),
                        )
                    )
                    .order_by("orden", "id"),
                )
            )
        )

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        paradas = list(self.object.paradas.all())
        if not paradas:
            messages.warning(
                request, "El itinerario no contiene paradas para exportar"
            )
            return redirect("itinerarios:itinerario_lista")

        styles = getSampleStyleSheet()
        styles.add(
            ParagraphStyle(
                name="RouteTitle",
                parent=styles["Title"],
                alignment=TA_CENTER,
                spaceAfter=8 * mm,
            )
        )
        styles.add(
            ParagraphStyle(
                name="RouteCell",
                parent=styles["BodyText"],
                fontSize=8,
                leading=10,
            )
        )
        styles.add(
            ParagraphStyle(
                name="RouteHeader",
                parent=styles["BodyText"],
                fontName="Helvetica-Bold",
                fontSize=8,
                textColor=colors.white,
            )
        )

        itinerario = self.object
        codigo = f"IT-{itinerario.fecha:%Y}-{itinerario.pk:05d}"
        transportista = itinerario.transportista
        nombre_transportista = (
            transportista.usuario.get_full_name() or transportista.usuario.username
            if transportista
            else "Sin asignar"
        )
        dni = transportista.usuario.username if transportista else "—"
        vehiculo = itinerario.vehiculo
        datos_vehiculo = (
            " - ".join(
                value
                for value in (vehiculo.modelo, vehiculo.patente)
                if value
            )
            if vehiculo
            else "Sin asignar"
        )

        historia = [
            Paragraph("HOJA DE RUTA", styles["RouteTitle"]),
            Table(
                [
                    [
                        Paragraph(f"<b>Itinerario:</b> {codigo}", styles["RouteCell"]),
                        Paragraph(
                            f"<b>Fecha de entrega:</b> {itinerario.fecha:%d/%m/%Y}",
                            styles["RouteCell"],
                        ),
                    ],
                    [
                        Paragraph(
                            f"<b>Transportista:</b> {escape(nombre_transportista)}",
                            styles["RouteCell"],
                        ),
                        Paragraph(f"<b>DNI:</b> {escape(dni)}", styles["RouteCell"]),
                    ],
                    [
                        Paragraph(
                            f"<b>Vehículo:</b> {escape(datos_vehiculo)}",
                            styles["RouteCell"],
                        ),
                        "",
                    ],
                ],
                colWidths=[93 * mm, 93 * mm],
                style=TableStyle(
                    [
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                    ]
                ),
            ),
            Spacer(1, 6 * mm),
        ]

        filas = [
            [
                Paragraph("N°", styles["RouteHeader"]),
                Paragraph("Comercio y domicilio", styles["RouteHeader"]),
                Paragraph("Remito(s)", styles["RouteHeader"]),
                Paragraph("Total a cobrar", styles["RouteHeader"]),
            ]
        ]
        total_itinerario = Decimal("0.00")
        for numero, parada in enumerate(paradas, start=1):
            remitos = list(parada.remitos.all())
            total_parada = sum(
                (remito.total for remito in remitos), Decimal("0.00")
            )
            total_itinerario += total_parada
            numeros_remito = "<br/>".join(
                escape(remito.numero) for remito in remitos
            ) or "Sin remitos"
            filas.append(
                [
                    Paragraph(str(numero), styles["RouteCell"]),
                    Paragraph(
                        f"<b>{escape(parada.comercio.razon_social)}</b><br/>"
                        f"{escape(parada.comercio.domicilio)}",
                        styles["RouteCell"],
                    ),
                    Paragraph(numeros_remito, styles["RouteCell"]),
                    Paragraph(f"${total_parada:.2f}", styles["RouteCell"]),
                ]
            )

        filas.append(
            [
                "",
                "",
                Paragraph("<b>Total del itinerario</b>", styles["RouteCell"]),
                Paragraph(f"<b>${total_itinerario:.2f}</b>", styles["RouteCell"]),
            ]
        )
        tabla_paradas = Table(
            filas,
            colWidths=[12 * mm, 86 * mm, 58 * mm, 30 * mm],
            repeatRows=1,
        )
        tabla_paradas.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#234B6B")),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#AAB7C4")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("ALIGN", (0, 1), (0, -1), "CENTER"),
                    ("ALIGN", (-1, 1), (-1, -1), "RIGHT"),
                    ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#EAF0F5")),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        historia.append(tabla_paradas)
        historia.extend(
            [
                Spacer(1, 10 * mm),
                Table(
                    [
                        ["Observaciones operativas", "Firma de conformidad del transportista"],
                        ["", ""],
                    ],
                    colWidths=[105 * mm, 81 * mm],
                    rowHeights=[9 * mm, 30 * mm],
                    style=TableStyle(
                        [
                            ("BOX", (0, 0), (-1, -1), 0.75, colors.black),
                            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.black),
                            ("VALIGN", (0, 0), (-1, -1), "TOP"),
                            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                            ("FONTSIZE", (0, 0), (-1, -1), 8),
                            ("LEFTPADDING", (0, 0), (-1, -1), 5),
                        ]
                    ),
                ),
            ]
        )

        buffer = BytesIO()
        document = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=12 * mm,
            leftMargin=12 * mm,
            topMargin=12 * mm,
            bottomMargin=12 * mm,
            title=f"Hoja de Ruta {codigo}",
        )
        document.build(historia)

        response = HttpResponse(buffer.getvalue(), content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="Hoja_Ruta_{codigo}.pdf"'
        )
        return response


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
                        if Cobranza.objects.filter(parada=parada).exists():
                            messages.error(
                                request,
                                "No se puede eliminar la parada porque posee cobranzas o rendiciones registradas.",
                            )
                        else:
                            itinerario = parada.itinerario
                            parada_id = parada.id
                            comercio_nombre = parada.comercio.razon_social
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
                if Cobranza.objects.filter(parada=parada).exists():
                    messages.error(
                        request,
                        f"No se puede quitar la parada de «{parada.comercio.razon_social}» porque posee cobranzas o rendiciones registradas.",
                    )
                    return redirect("itinerarios:itinerario_editar", pk=itinerario.pk)

                comercio_nombre = parada.comercio.razon_social
                with transaction.atomic():
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

        if itinerario.estado in [EstadoItinerario.FINALIZADO, EstadoItinerario.EN_CURSO]:
            messages.error(
                request, f"No se puede eliminar un itinerario en estado '{itinerario.get_estado_display()}'."
            )
            return redirect("itinerarios:itinerario_lista")

        if Cobranza.objects.filter(parada__itinerario=itinerario).exists():
            messages.error(
                request,
                "No se puede eliminar el itinerario porque posee cobranzas o rendiciones registradas.",
            )
            return redirect("itinerarios:itinerario_lista")

        if itinerario.paradas.filter(estado=EstadoParada.FINALIZADA).exists():
            messages.error(
                request,
                "No se puede eliminar el itinerario porque contiene paradas que ya fueron finalizadas.",
            )
            return redirect("itinerarios:itinerario_lista")

        try:
            with transaction.atomic():
                Remito.objects.filter(parada__itinerario=itinerario).exclude(
                    estado=EstadoRemito.ENTREGADO
                ).update(
                    parada=None,
                    estado=EstadoRemito.PENDIENTE,
                )
                itinerario.delete()
            messages.success(request, "Itinerario eliminado exitosamente")
        except (ProtectedError, DatabaseError):
            messages.error(
                request,
                "No se puede eliminar el itinerario debido a restricciones de integridad de datos.",
            )

        return redirect("itinerarios:itinerario_lista")

    def get(self, request, pk, *args, **kwargs):
        return redirect("itinerarios:itinerario_lista")
