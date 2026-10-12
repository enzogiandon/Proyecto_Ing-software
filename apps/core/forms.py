from django.contrib.auth.forms import AuthenticationForm

from .models import Usuario


class LoginForm(AuthenticationForm):
    error_messages = {
        "invalid_login": "El usuario o la contraseña ingresados son incorrectos. Inténtalo de nuevo.",
        "inactive": "Esta cuenta se encuentra suspendida.",
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Usuario"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Contraseña"}
        )

    def get_user(self) -> Usuario:
        user = super().get_user()
        assert isinstance(user, Usuario)
        return user
