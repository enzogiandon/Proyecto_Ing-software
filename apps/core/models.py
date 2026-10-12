from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from simple_history.models import HistoricalRecords


class Usuario(AbstractUser):
    telefono = models.CharField(max_length=10)
    dni_validator = RegexValidator(
        regex=r"^\d{7,8}$",
        message="El DNI debe contener 7 u 8 dígitos sin puntos ni guiones.",
    )
    dni = models.CharField(
        max_length=8,
        unique=True,
        validators=[dni_validator],
    )
    intentos_fallidos = models.IntegerField(default=0)
    history = HistoricalRecords()
