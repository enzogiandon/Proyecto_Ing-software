import csv
import io
import os
from decimal import Decimal

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from apps.itinerarios.models import EstadoParada, Parada

from .forms import (
    ComercioForm,
    ImportacionRemitosForm,
    MarcaForm,
    RemitoForm,
)
from .models import (
    Comercio,
    ErrorImportacion,
    EstadoImportacion,
    EstadoRemito,
    ImportacionRemitos,
    Marca,
    Remito,
)


class CrearRemito(CreateView):
    form_class = RemitoForm
    template_name = "remitos/remito_form.html"

    success_url = reverse_lazy("remitos:remito_lista")

    permission_required = ""
    raise_exception = True

    def form_valid(self, form):
        comercio = form.cleaned_data.get("comercio")
        parada_existente = Parada.objects.filter(
            comercio=comercio,
            estado=EstadoParada.PENDIENTE,
        ).first()

        if parada_existente:
            form.instance.parada = parada_existente
            form.instance.estado = EstadoRemito.ASIGNADO
        else:
            form.instance.parada = None
            form.instance.estado = EstadoRemito.PENDIENTE

        return super().form_valid(form)


class EditarRemito(UpdateView):
    form_class = RemitoForm
    model = Remito
    template_name = "remitos/remito_form.html"

    success_url = reverse_lazy("remitos:remito_lista")

    permission_required = ""
    raise_exception = True


class DetalleRemito(DetailView):
    model = Remito
    template_name = "remitos/remito_detalle.html"
    context_object_name = "remito"


class ListaRemito(ListView):
    model = Remito
    template_name = "remitos/remito_lista.html"
    context_object_name = "remitos"
    paginate_by = 25

    def get_queryset(self):
        qs = (
            super()
            .get_queryset()
            .select_related("comercio", "marca")
            .order_by("-id")
        )

        comercio = self.request.GET.get("comercio", "").strip()
        estado = self.request.GET.get("estado", "").strip()
        marca = self.request.GET.get("marca", "").strip()
        fecha = self.request.GET.get("fecha", "").strip()

        if comercio:
            qs = qs.filter(comercio__razon_social__icontains=comercio)
        if estado:
            qs = qs.filter(estado=estado)
        if marca:
            qs = qs.filter(marca_id=marca)
        if fecha:
            qs = qs.filter(fecha_creacion__date=fecha)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Opciones para los desplegables
        context["estados"] = EstadoRemito.choices
        context["marcas"] = Marca.objects.all().order_by("nombre")

        # Variables para mantener el estado del formulario en el HTML
        context["filtro_comercio"] = self.request.GET.get("comercio", "")
        context["filtro_estado"] = self.request.GET.get("estado", "")
        context["filtro_marca"] = self.request.GET.get("marca", "")
        context["filtro_fecha"] = self.request.GET.get("fecha", "")
        return context


class EliminarRemito(DeleteView):
    model = Remito
    template_name = "remitos/remito_eliminar.html"
    success_url = reverse_lazy("remitos:remito_lista")

    def form_valid(self, form):
        remito = self.get_object()
        parada = remito.parada
        resultado = super().form_valid(form)

        if parada and parada.estado == EstadoParada.PENDIENTE and not parada.remitos.filter(eliminado=False).exists():
            itinerario = parada.itinerario
            parada.delete()
            for i, p in enumerate(
                itinerario.paradas.all().order_by("orden", "id"), start=1
            ):
                p.orden = i
                p.save(update_fields=["orden"])

        return resultado


class ImportarRemitos(CreateView):
    form_class = ImportacionRemitosForm
    model = ImportacionRemitos
    template_name = "remitos/importar_csv.html"
    success_url = reverse_lazy("core:inicio")

    def form_valid(self, form):
        archivos = self.request.FILES.getlist("archivo")
        marca_seleccionada = form.cleaned_data.get("marca")

        creados = 0
        total_remitos_creados = 0
        lotes_guardados = 0
        errores = []

        for archivo in archivos:
            nombre_archivo = os.path.basename(archivo.name)
            cuit_marca = nombre_archivo.split("_")[0].strip()

            marca = Marca.objects.filter(cuit=cuit_marca).first()
            if not marca:
                marca = marca_seleccionada

            if not marca:
                errores.append(
                    f"No se encontró la marca con CUIT {cuit_marca} para el archivo {nombre_archivo}."
                )
                continue

            try:
                archivo.seek(0)
                wrapper = io.TextIOWrapper(archivo, encoding="utf-8-sig")
                reader = csv.DictReader(wrapper)

                filas = list(reader)
                if not filas:
                    raise ValueError(f"El archivo {nombre_archivo} está vacío.")

                errores_filas = []
                datos_validados = []

                for fila_num, row in enumerate(filas, start=2):
                    cuit_comercio = row.get("cuit_comercio", "").strip()
                    razon_social = row.get("razon_social", "").strip()
                    domicilio = row.get("domicilio", "").strip()
                    monto_str = row.get("monto_a_cobrar", "").strip()
                    num_sucursal = row.get("numero_sucursal", "").strip()
                    num_factura = row.get("numero_factura", "").strip()

                    motivos = []
                    if not cuit_comercio or not cuit_comercio.isdigit() or len(cuit_comercio) != 11:
                        motivos.append("CUIT del comercio inválido (debe tener 11 dígitos numéricos)")

                    total_monto = None
                    try:
                        total_monto = Decimal(monto_str)
                        if total_monto <= Decimal("0.00"):
                            motivos.append("El monto a cobrar debe ser mayor a cero")
                    except Exception:
                        motivos.append(f"Monto a cobrar inválido: '{monto_str}'")

                    if not num_sucursal or not num_factura:
                        motivos.append("Falta número de sucursal o factura")

                    if motivos:
                        errores_filas.append((fila_num, "; ".join(motivos)))
                    else:
                        numero_remito = f"{num_sucursal}-{num_factura}"
                        datos_validados.append(
                            {
                                "cuit_comercio": cuit_comercio,
                                "razon_social": razon_social,
                                "domicilio": domicilio,
                                "total": total_monto,
                                "numero": numero_remito,
                            }
                        )

                archivo.seek(0)

                with transaction.atomic():
                    importacion = ImportacionRemitos.objects.create(
                        archivo=archivo,
                        marca=marca,
                        estado=EstadoImportacion.RECHAZADO if errores_filas else EstadoImportacion.PENDIENTE,
                        cantidad=0,
                    )
                    lotes_guardados += 1

                    if errores_filas:
                        for f_num, mot in errores_filas:
                            ErrorImportacion.objects.create(
                                importacion=importacion,
                                fila=f_num,
                                motivo=mot,
                            )
                        errores.append(
                            f"El archivo {nombre_archivo} contiene {len(errores_filas)} errores y fue rechazado (Lote #{importacion.id})."
                        )
                    else:
                        remitos_creados_lote = 0
                        for d in datos_validados:
                            comercio, _ = Comercio.objects.get_or_create(
                                cuit=d["cuit_comercio"],
                                defaults={
                                    "razon_social": d["razon_social"],
                                    "domicilio": d["domicilio"],
                                    "activo": True,
                                },
                            )

                            Remito.objects.create(
                                numero=d["numero"],
                                marca=marca,
                                comercio=comercio,
                                total=d["total"],
                                estado=EstadoRemito.PENDIENTE,
                                parada=None,
                                importacion=importacion,
                                eliminado=False,
                            )
                            remitos_creados_lote += 1

                        importacion.cantidad = remitos_creados_lote
                        importacion.estado = EstadoImportacion.EXITO
                        importacion.save(update_fields=["cantidad", "estado"])

                        creados += 1
                        total_remitos_creados += remitos_creados_lote

            except Exception as e:
                errores.append(f"Error procesando {nombre_archivo}: {str(e)}")

        if errores:
            for error in errores:
                messages.error(self.request, error)

        if creados > 0:
            if creados == 1:
                messages.success(
                    self.request,
                    f"La planilla se procesó correctamente ({total_remitos_creados} remitos pendientes creados).",
                )
            else:
                messages.success(
                    self.request,
                    f"Se procesaron correctamente {creados} planillas ({total_remitos_creados} remitos pendientes creados en total).",
                )

        if creados == 0 and not lotes_guardados and errores:
            return self.form_invalid(form)

        return redirect(self.success_url)


class ListaImportacion(ListView):
    model = ImportacionRemitos
    template_name = "remitos/importacion_lista.html"
    context_object_name = "importaciones"
    paginate_by = 25

    def get_queryset(self):
        return (
            ImportacionRemitos.objects.select_related("marca")
            .all()
            .order_by("-fecha", "-id")
        )


class DetalleImportacion(DetailView):
    model = ImportacionRemitos
    template_name = "remitos/importacion_detalle.html"
    context_object_name = "importacion"

    def get_queryset(self):
        return super().get_queryset().prefetch_related("errores")


class EliminarImportacion(DeleteView):
    model = ImportacionRemitos
    template_name = "remitos/importacion_eliminar.html"
    success_url = reverse_lazy("remitos:importacion_lista")


class CrearComercio(SuccessMessageMixin, CreateView):
    form_class = ComercioForm
    model = Comercio
    template_name = "remitos/comercio_crear.html"
    context_object_name = "comercios"
    success_url = reverse_lazy("remitos:comercio_lista")
    success_message = "Comercio agregado exitosamente"


class ListaComercio(ListView):
    model = Comercio
    template_name = "remitos/comercio_lista.html"
    context_object_name = "comercios"
    paginate_by = 25

    def get_queryset(self):
        return Comercio.objects.all().order_by("-activo", "-id")


class EditarComercio(UpdateView):
    form_class = ComercioForm
    model = Comercio
    template_name = "remitos/comercio_form.html"
    success_url = reverse_lazy("remitos:comercio_lista")


class EliminarComercio(DeleteView):
    model = Comercio
    template_name = "remitos/comercio_eliminar.html"
    success_url = reverse_lazy("remitos:comercio_lista")


class CrearMarca(SuccessMessageMixin, CreateView):
    form_class = MarcaForm
    model = Marca
    template_name = "remitos/marca_crear.html"
    context_object_name = "marcas"
    success_url = reverse_lazy("remitos:marca_lista")
    success_message = "Marca agregado exitosamente"


class ListaMarca(ListView):
    model = Marca
    template_name = "remitos/marca_lista.html"
    context_object_name = "marcas"
    paginate_by = 25

    def get_queryset(self):
        return Marca.objects.all().order_by("-activo", "-id")


class EditarMarca(UpdateView):
    form_class = MarcaForm
    model = Marca
    template_name = "remitos/marca_form.html"
    success_url = reverse_lazy("remitos:marca_lista")


class EliminarMarca(DeleteView):
    model = Marca
    template_name = "remitos/marca_eliminar.html"
    success_url = reverse_lazy("remitos:marca_lista")
