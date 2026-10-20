from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, TemplateView

from .forms import LoginForm, UserRegisterForm
from .models import Usuario

# Create your views here.

class CustomLoginView(LoginView):
    template_name = "core/login.html"
    form_class = LoginForm
    #redirect_authenticated_user = True


    def form_valid(self, form):
        user = form.get_user()
        user.last_login = timezone.now()
        user.intentos_fallidos = 0
        user.save(update_fields=["last_login", "intentos_fallidos"])
        return super().form_valid(form)

    def form_invalid(self, form):
        username = form.cleaned_data.get("username")

        try:
            user = Usuario.objects.get(username=username)
            if user.is_active:
                user.intentos_fallidos += 1
                if user.intentos_fallidos >= 5:
                    user.is_active = False
            user.save(update_fields=["intentos_fallidos", "is_active"])

        except ObjectDoesNotExist:
            pass
        return super().form_invalid(form)

class CrearUsuario(CreateView):
    form_class = UserRegisterForm
    template_name = "core/crear_usuario.html"

    success_url = reverse_lazy("")

    permission_required = ""
    raise_exception = True

class Inicio(LoginRequiredMixin, TemplateView):
    template_name = "core/inicio.html"
    login_url = reverse_lazy("core:login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["username"] = user.first_name or user.username
        return context
