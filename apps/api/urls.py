# apps/api/urls.py
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import ItinerarioViewSet, ParadaViewSet

app_name = "api"

router = routers.DefaultRouter()
router.register(r"itinerarios", ItinerarioViewSet, basename="itinerario")
router.register(r"paradas", ParadaViewSet, basename="parada")

urlpatterns = [
    # Rutas generadas por el router de DRF (/api/users/, /api/groups/, etc.)
    path("", include(router.urls)),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "api-auth/",
        include("rest_framework.urls", namespace="rest_framework"),
    ),
]
