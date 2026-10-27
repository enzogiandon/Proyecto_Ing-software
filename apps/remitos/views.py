from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import (
    ComercioForm,
    ImportacionRemitosForm,
    MarcaForm,
    RemitoForm,
)
from .models import Comercio, ImportacionRemitos, Marca, Remito


class CrearRemito(CreateView):
    form_class = RemitoForm
    template_name = "remitos/remito_form.html"

    success_url = reverse_lazy("remitos:remito_lista")

    permission_required = ""
    raise_exception = True


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
        return (
            Remito.objects.select_related("marca", "comercio", "parada")
            .all()
            .order_by("id")
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
