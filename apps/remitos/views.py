from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import ImportacionRemitosForm, ItemRemitoFormSet, RemitoForm
from .models import ImportacionRemitos, Remito


class CrearRemito(CreateView):
    form_class = RemitoForm 
    template_name = "remitos/remito_form.html"

    success_url = reverse_lazy("core:inicio")

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
        items_formset = context ["items_formset"]
        if items_formset.is_valid():
            with transaction.atomic():
                self.object = form.save()
                items_formset.instance = self.object
                items_formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))



class EditarRemito(UpdateView):
    form_class = RemitoForm
    model = Remito
    template_name = "remitos/remito_form.html"

    success_url = reverse_lazy("core:inicio")

    permission_required = ""
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["items_formset"] = ItemRemitoFormSet(self.request.POST, instance=self.object)
        else:
            context["items_formset"] = ItemRemitoFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        items_formset = context ["items_formset"]
        if items_formset.is_valid():
            with transaction.atomic():
                self.object = form.save()
                items_formset.istance = self.object
                items_formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class DetalleRemito(DetailView):
    model = Remito
    template_name = "remitos/remito_detalle.html"
    context_objet_name = ( "remito" )

class ListaRemito(ListView):
    model = Remito
    template_name = "remitos/remito_lista.html"
    context_object_name = ( "remitos" )
    paginate_by = 25

    def get_queryset(self):
        return Remito.objects.select_related("marca", "comercio", "parada").all().order_by("-fecha_creacion", "id")

class ImportarRemitos(SuccessMessageMixin, CreateView):
    form_class = ImportacionRemitosForm
    model = ImportacionRemitos
    template_name = "remitos/importar_csv.html"
    success_url = reverse_lazy("core:inicio")
    success_message = "La planilla se guardo correctamente"


class ListaImportacion(ListView):
    model = ImportacionRemitos
    template_name = "remitos/importacion_lista.html"
    context_object_name = ( "importaciones" )
    paginate_by = 25

    def get_queryset(self):
        return ImportacionRemitos.objects.select_related("marca").all().order_by("-fecha", "-id")
