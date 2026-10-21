from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    View,
)

from .forms import (
    ComercioForm,
    ImportacionRemitosForm,
    ItemRemitoFormSet,
    MarcaForm,
    ProductoForm,
    RemitoForm,
)
from .models import Comercio, ImportacionRemitos, Marca, Producto, Remito


class CrearRemito(CreateView):
    form_class = RemitoForm
    template_name = "remitos/remito_form.html"

    success_url = reverse_lazy("remitos:remito_lista")

    permission_required = ""
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["items_formset"] = ItemRemitoFormSet(self.request.POST)
        else:
            context["items_formset"] = ItemRemitoFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        items_formset = context["items_formset"]
        if items_formset.is_valid():
            items_validos = [
                f
                for f in items_formset.forms
                if f.cleaned_data and not f.cleaned_data.get("DELETE", False)
            ]
            if not items_validos:
                form.add_error(
                    None, "El remito tiene que tener por lo menos un producto"
                )

                return self.form_invalid(form)

            with transaction.atomic():
                self.object = form.save()
                items_formset.instance = self.object
                items_formset.save()
                assert self.object is not None
                self.object.actualizar_monto_total()

            return super().form_valid(form)
        else:
            context = self.get_context_data(form=form)
            context["items_formset"] = items_formset
            return self.render_to_response(context)


class EditarRemito(UpdateView):
    form_class = RemitoForm
    model = Remito
    template_name = "remitos/remito_form.html"

    success_url = reverse_lazy("remitos:remito_lista")

    permission_required = ""
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["items_formset"] = ItemRemitoFormSet(
                self.request.POST, instance=self.object
            )
        else:
            context["items_formset"] = ItemRemitoFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        items_formset = context["items_formset"]
        if items_formset.is_valid():
            with transaction.atomic():
                self.object = form.save()
                items_formset.save()
                self.object.actualizar_monto_total()

            return super().form_valid(form)
        else:
            context = self.get_context_data(form=form)
            context["items_formset"] = items_formset
            return self.render_to_response(context)


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
        return (
            Remito.objects.select_related("marca", "comercio", "parada")
            .all()
            .order_by("-fecha_creacion", "id")
        )


class EliminarRemito(DeleteView):
    model = Remito
    template_name = "remitos/remito_eliminar.html"
    success_url = reverse_lazy("remitos:remito_lista")


class ImportarRemitos(SuccessMessageMixin, CreateView):
    form_class = ImportacionRemitosForm
    model = ImportacionRemitos
    template_name = "remitos/importar_csv.html"
    success_url = reverse_lazy("core:inicio")
    success_message = "La planilla se guardo correctamente"


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


class DetalleImportacion(View):
    model = ImportacionRemitos
    template_name = "remitos/importacion_detalle.html"
    context_object_name = "importacion"


class EliminarImportacion(DeleteView):
    model = ImportacionRemitos
    template_name = "remitos/importacion_eliminar.html"
    success_url = reverse_lazy("remitos:importacion_lista")


class CrearProducto(SuccessMessageMixin, CreateView):
    form_class = ProductoForm
    model = Producto
    template_name = "remitos/producto_form.html"
    success_url = reverse_lazy("remitos:producto_lista")
    success_message = "Producto agregado exitosamente"


class ListaProducto(ListView):
    model = Producto
    template_name = "remitos/producto_lista.html"
    context_object_name = "productos"
    paginate_by = 25

    def get_queryset(self):
        return Producto.objects.all().order_by("-activo", "-id")


class EditarProducto(UpdateView):
    form_class = ProductoForm
    model = Producto
    template_name = "remitos/producto_form.html"
    success_url = reverse_lazy("remitos:producto_lista")


class EliminarProducto(DeleteView):
    model = Producto
    template_name = "remitos/producto_eliminar.html"
    success_url = reverse_lazy("remitos:producto_lista")


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
    context_object_name = "productos"
    paginate_by = 25

    def get_queryset(self):
        return Comercio.objects.all().order_by("-activo", "-id")


class EditarComercio(UpdateView):
    form_class = ProductoForm
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
    context_object_name = "productos"
    paginate_by = 25

    def get_queryset(self):
        return Marca.objects.all().order_by("-activo", "-id")


class EditarMarca(UpdateView):
    form_class = ProductoForm
    model = Marca
    template_name = "remitos/marca_form.html"
    success_url = reverse_lazy("remitos:marca_lista")


class EliminarMarca(DeleteView):
    model = Marca
    template_name = "remitos/marca_eliminar.html"
    success_url = reverse_lazy("remitos:marca_lista")
