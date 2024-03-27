from django.urls import path, include
from rest_framework import routers

from .views import ShowThemeViewSet, AstronomyShowViewSet, PlanetariumDomeViewSet

router = routers.DefaultRouter()

router.register("show_themes", ShowThemeViewSet)
router.register("astronomy_shows", AstronomyShowViewSet)
router.register("planetarium_domes", PlanetariumDomeViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "planetarium"
