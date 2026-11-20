import csv
import io
import os
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ValidationError
from django.db import DatabaseError, IntegrityError, transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
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


class CrearRemito(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = RemitoForm
    template_name = "remitos/remito_form.html"
    success_url = reverse_lazy("remitos:remito_lista")
    permission_required = "remitos.add_remito"

    def form_valid(self, form):
        form.instance.parada = None
        form.instance.estado = EstadoRemito.PENDIENTE
        return super().form_valid(form)


class EditarRemito(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = RemitoForm
    model = Remito
    template_name = "remitos/remito_form.html"
    permission_required = "remitos.change_remito"

    def get_success_url(self):
        return reverse_lazy("remitos:remito_detalle", kwargs={"pk": self.object.pk})

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.estado != EstadoRemito.PENDIENTE:
            messages.error(request, "Solo editable en estado pendiente")
            return redirect("remitos:remito_detalle", pk=self.object.pk)
            
        return super().dispatch(request, *args, **kwargs)


class DetalleRemito(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Remito
    template_name = "remitos/remito_detalle.html"
    context_object_name = "remito"
    permission_required = "remitos.view_remito"


class ListaRemito(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Remito
    template_name = "remitos/remito_lista.html"
    context_object_name = "remitos"
    paginate_by = 25
    permission_required = "remitos.view_remito"

    def get_queryset(self):
        qs = super().get_queryset().select_related("comercio", "marca").order_by("-id")

        comercio = self.request.GET.get("comercio", "").strip()
        estado = self.request.GET.get("estado", "").strip()
        marca = self.request.GET.get("marca", "").strip()

        if comercio:
            qs = qs.filter(comercio__razon_social__icontains=comercio)
        if estado:
            qs = qs.filter(estado=estado)
        if marca:
            qs = qs.filter(marca_id=marca)

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
        return context


class EliminarRemito(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Remito
    template_name = "remitos/remito_eliminar.html"
    success_url = reverse_lazy("remitos:remito_lista")
    permission_required = "remitos.delete_remito"

    def form_valid(self, form):
        remito = self.get_object()
        parada = remito.parada
        resultado = super().form_valid(form)

        if (
            parada
            and parada.estado == EstadoParada.PENDIENTE
            and not parada.remitos.exists()
        ):
            itinerario = parada.itinerario
            parada.delete()
            for i, p in enumerate(
                itinerario.paradas.all().order_by("orden", "id"), start=1
            ):
                p.orden = i
                p.save(update_fields=["orden"])

        return resultado


class ImportarRemitos(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = ImportacionRemitosForm
    model = ImportacionRemitos
    template_name = "remitos/importar_csv.html"
    success_url = reverse_lazy("core:inicio")
    permission_required = "remitos.add_importacionremitos"

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

            if not marca.activo:
                errores.append(
                    f"La marca {marca.nombre} (CUIT {marca.cuit}) se encuentra inactiva."
                )
                continue

            try:
                archivo.seek(0)
                wrapper = io.TextIOWrapper(archivo, encoding="utf-8-sig")
                reader = csv.DictReader(wrapper)

                filas = list(reader)
                if not filas:
                    raise ValueError(f"El archivo {nombre_archivo} está vacío.")

                columnas_requeridas = {
                    "cuit_comercio",
                    "razon_social",
                    "domicilio",
                    "monto_a_cobrar",
                    "numero_sucursal",
                    "numero_factura",
                }
                columnas_archivo = set(reader.fieldnames or [])
                if not columnas_requeridas.issubset(columnas_archivo):
                    archivo.seek(0)
                    with transaction.atomic():
                        importacion = ImportacionRemitos.objects.create(
                            archivo=archivo,
                            marca=marca,
                            estado=EstadoImportacion.RECHAZADO,
                            cantidad=0,
                        )
                        lotes_guardados += 1
                        ErrorImportacion.objects.create(
                            importacion=importacion,
                            fila=1,
                            motivo="Importación fallida: la estructura del archivo seleccionado es inválida.",
                        )
                    errores.append(
                        "Importación fallida: la estructura del archivo seleccionado es inválida"
                    )
                    continue

                errores_filas = []
                datos_validados = []
                numeros_en_archivo = set()

                # Extraer CUITs válidos del archivo para consultar cuáles ya existen en la base de datos
                cuits_en_filas = set()
                for row in filas:
                    cuit = (row.get("cuit_comercio") or "").strip()
                    if cuit.isdigit() and len(cuit) == 11:
                        cuits_en_filas.add(cuit)

                cuits_existentes_db = set(
                    Comercio.objects.filter(cuit__in=cuits_en_filas).values_list(
                        "cuit", flat=True
                    )
                )

                for fila_num, row in enumerate(filas, start=2):
                    cuit_comercio = (row.get("cuit_comercio") or "").strip()
                    razon_social = (row.get("razon_social") or "").strip()
                    domicilio = (row.get("domicilio") or "").strip()
                    monto_str = (row.get("monto_a_cobrar") or "").strip()
                    num_sucursal = (row.get("numero_sucursal") or "").strip()
                    num_factura = (row.get("numero_factura") or "").strip()

                    motivos = []
                    if (
                        not cuit_comercio
                        or not cuit_comercio.isdigit()
                        or len(cuit_comercio) != 11
                    ):
                        motivos.append(
                            "CUIT del comercio inválido (debe tener 11 dígitos numéricos)"
                        )
                    elif cuit_comercio not in cuits_existentes_db and not razon_social:
                        motivos.append(
                            "La razón social es obligatoria para comercios no registrados"
                        )

                    total_monto = None
                    try:
                        total_monto = Decimal(monto_str)
                        if total_monto <= Decimal("0.00"):
                            motivos.append("El monto a cobrar debe ser mayor a cero")
                    except (InvalidOperation, TypeError):
                        motivos.append(f"Monto a cobrar inválido: '{monto_str}'")

                    if not num_sucursal or not num_factura:
                        motivos.append("Falta número de sucursal o factura")
                    else:
                        num_sucursal_pad = num_sucursal.zfill(4) if num_sucursal.isdigit() else num_sucursal
                        num_factura_pad = num_factura.zfill(8) if num_factura.isdigit() else num_factura
                        numero_remito = f"{num_sucursal_pad}-{num_factura_pad}"
                        if numero_remito in numeros_en_archivo:
                            motivos.append(f"Número de remito '{numero_remito}' duplicado dentro del mismo archivo")
                        else:
                            numeros_en_archivo.add(numero_remito)

                    if motivos:
                        errores_filas.append((fila_num, "; ".join(motivos)))
                    else:
                        datos_validados.append(
                            {
                                "cuit_comercio": cuit_comercio,
                                "razon_social": razon_social,
                                "domicilio": domicilio,
                                "total": total_monto,
                                "numero": numero_remito,
                            }
                        )

                if not errores_filas and datos_validados:
                    existentes = set(
                        Remito.objects.filter(
                            marca=marca,
                            numero__in=numeros_en_archivo,
                        ).values_list("numero", flat=True)
                    )
                    if existentes:
                        for idx, d in enumerate(datos_validados, start=2):
                            if d["numero"] in existentes:
                                errores_filas.append(
                                    (idx, "El número de remito debe ser único por marca proveedora.")
                                )

                archivo.seek(0)

                with transaction.atomic():
                    importacion = ImportacionRemitos.objects.create(
                        archivo=archivo,
                        marca=marca,
                        estado=EstadoImportacion.RECHAZADO
                        if errores_filas
                        else EstadoImportacion.PENDIENTE,
                        cantidad=0,
                    )
                    lotes_guardados += 1

                    if errores_filas:
                        errores_objs = [
                            ErrorImportacion(
                                importacion=importacion,
                                fila=f_num,
                                motivo=mot,
                            )
                            for f_num, mot in errores_filas
                        ]
                        ErrorImportacion.objects.bulk_create(errores_objs, batch_size=100)
                        errores.append(
                            f"Importación rechazada: se detectaron {len(errores_filas)} errores en las filas observadas de {nombre_archivo}. Corrija el archivo e intente nuevamente."
                        )
                    else:
                        # 1. Obtener comercios existentes y crear los que falten en bloque
                        cuits_en_archivo = {d["cuit_comercio"] for d in datos_validados}
                        comercios_existentes = {
                            c.cuit: c
                            for c in Comercio.objects.filter(cuit__in=cuits_en_archivo)
                        }

                        comercios_a_crear = []
                        cuits_por_crear = set()
                        for d in datos_validados:
                            cuit = d["cuit_comercio"]
                            if cuit not in comercios_existentes and cuit not in cuits_por_crear:
                                cuits_por_crear.add(cuit)
                                comercios_a_crear.append(
                                    Comercio(
                                        cuit=cuit,
                                        razon_social=d["razon_social"],
                                        domicilio=d["domicilio"],
                                        activo=True,
                                    )
                                )

                        if comercios_a_crear:
                            Comercio.objects.bulk_create(comercios_a_crear, batch_size=1000)
                            for c in Comercio.objects.filter(cuit__in=cuits_por_crear):
                                comercios_existentes[c.cuit] = c

                        # 2. Crear todos los remitos del lote en bloque
                        remitos_a_crear = [
                            Remito(
                                numero=d["numero"],
                                marca=marca,
                                comercio=comercios_existentes[d["cuit_comercio"]],
                                total=d["total"],
                                estado=EstadoRemito.PENDIENTE,
                                parada=None,
                                importacion=importacion,
                            )
                            for d in datos_validados
                        ]

                        Remito.objects.bulk_create(remitos_a_crear, batch_size=1000)
                        remitos_creados_lote = len(remitos_a_crear)

                        importacion.cantidad = remitos_creados_lote
                        importacion.estado = EstadoImportacion.EXITO
                        importacion.save(update_fields=["cantidad", "estado"])

                        creados += 1
                        total_remitos_creados += remitos_creados_lote

            except (UnicodeDecodeError, csv.Error, ValueError):
                errores.append(f"El archivo {nombre_archivo} tiene un formato inválido o no legible.")
            except (IntegrityError, DatabaseError):
                errores.append(f"Error de base de datos al procesar {nombre_archivo}.")
            except OSError:
                errores.append(f"Error de lectura o acceso al archivo {nombre_archivo}.")

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


class ListaImportacion(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ImportacionRemitos
    template_name = "remitos/importacion_lista.html"
    context_object_name = "importaciones"
    paginate_by = 25
    permission_required = "remitos.view_importacionremitos"

    def get_queryset(self):
        return (
            ImportacionRemitos.objects.select_related("marca")
            .all()
            .order_by("-fecha", "-id")
        )


class DetalleImportacion(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = ImportacionRemitos
    template_name = "remitos/importacion_detalle.html"
    context_object_name = "importacion"
    permission_required = "remitos.view_importacionremitos"

    def get_queryset(self):
        return super().get_queryset().prefetch_related("errores", "remitos")


class EliminarImportacion(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = ImportacionRemitos
    template_name = "remitos/importacion_eliminar.html"
    success_url = reverse_lazy("remitos:importacion_lista")
    permission_required = "remitos.delete_importacionremitos"

    def _tiene_remitos_no_pendientes(self, importacion):
        # Verifica si existe al menos un remito cuyo estado NO sea 'pendiente'
        return (
            importacion.remitos.exclude(
                estado=EstadoRemito.PENDIENTE  # o "pendiente"
            )
            .exists()
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pasamos esta bandera al template para advertir al usuario y ocultar el botón de confirmar
        context["puede_eliminar"] = not self._tiene_remitos_no_pendientes(self.object)
        return context

    def form_valid(self, form):
        self.object = self.get_object()

        # Validación de seguridad en el POST
        if self._tiene_remitos_no_pendientes(self.object):
            messages.error(
                self.request,
                "La importación no se puede eliminar porque contiene remitos que ya fueron asignados a un itinerario.",
            )
            return redirect(self.success_url)

        with transaction.atomic():
            # Eliminación física de todos los remitos de esta importación
            self.object.remitos.all().delete()
            self.object.delete()

        messages.success(
            self.request, "La importación y sus remitos asociados fueron eliminados exitosamente."
        )
        return HttpResponseRedirect(self.get_success_url())


class CrearComercio(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = ComercioForm
    model = Comercio
    template_name = "remitos/comercio_crear.html"
    context_object_name = "comercios"
    success_url = reverse_lazy("remitos:comercio_lista")
    success_message = "Comercio agregado exitosamente"
    permission_required = "remitos.add_comercio"


class ListaComercio(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Comercio
    template_name = "remitos/comercio_lista.html"
    context_object_name = "comercios"
    paginate_by = 25
    permission_required = "remitos.view_comercio"

    def get_queryset(self):
        return Comercio.objects.all().order_by("-activo", "-id")


class EditarComercio(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = ComercioForm
    model = Comercio
    template_name = "remitos/comercio_form.html"
    success_url = reverse_lazy("remitos:comercio_lista")
    permission_required = "remitos.change_comercio"


class EliminarComercio(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Comercio
    template_name = "remitos/comercio_eliminar.html"
    success_url = reverse_lazy("remitos:comercio_lista")
    permission_required = "remitos.delete_comercio"


class CrearMarca(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = MarcaForm
    model = Marca
    template_name = "remitos/marca_form.html"
    success_url = reverse_lazy("remitos:marca_lista")
    success_message = "Marca agregada exitosamente"
    permission_required = "remitos.add_marca"


class ListaMarca(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Marca
    template_name = "remitos/marca_lista.html"
    context_object_name = "marcas"
    paginate_by = 25
    permission_required = "remitos.view_marca"

    def get_queryset(self):
        return Marca.objects.all().order_by("-activo", "-id")


class EditarMarca(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = MarcaForm
    model = Marca
    template_name = "remitos/marca_form.html"
    success_url = reverse_lazy("remitos:marca_lista")
    success_message = "Marca modificada exitosamente"
    permission_required = "remitos.change_marca"


class EliminarMarca(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Marca
    template_name = "remitos/marca_eliminar.html"
    success_url = reverse_lazy("remitos:marca_lista")
    permission_required = "remitos.delete_marca"

    def form_valid(self, form):
        marca = self.get_object()
        remitos_activos = marca.remitos.filter(
            estado__in=[EstadoRemito.PENDIENTE, EstadoRemito.ASIGNADO]
        )
        if remitos_activos.exists():
            messages.error(
                self.request,
                "No se puede eliminar la marca porque tiene remitos en estado pendiente o asignado.",
            )
            return redirect(self.success_url)

        marca.activo = False
        marca.save(update_fields=["activo"])
        messages.success(self.request, "Marca eliminada exitosamente")
        return redirect(self.success_url)


class ReactivarMarca(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "remitos.change_marca"

    def post(self, request, pk):
        marca = get_object_or_404(Marca, pk=pk)
        marca.activo = True
        marca.save(update_fields=["activo"])
        messages.success(request, "Marca reactivada exitosamente")
        return redirect("remitos:marca_lista")
