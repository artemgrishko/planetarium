from django.urls import path, include
from rest_framework import routers

from .views import (
    ShowThemeViewSet,
    AstronomyShowViewSet,
    PlanetariumDomeViewSet,
    ShowSessionViewSet,
    TicketViewSet, ReservationViewSet
)

router = routers.DefaultRouter()

router.register("showtheme", ShowThemeViewSet)
router.register("astronomyshow", AstronomyShowViewSet)
router.register("planetarium_domes", PlanetariumDomeViewSet)
router.register("show_session", ShowSessionViewSet)
router.register("tickets", TicketViewSet)
router.register("reservation", ReservationViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "planetarium"
