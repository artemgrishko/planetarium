from django.urls import path, include
from rest_framework import routers

from .views import ShowThemeViewSet, AstronomyShowViewSet

router = routers.DefaultRouter()

router.register("show_themes", ShowThemeViewSet)
router.register("astronomy_shows", AstronomyShowViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "planetarium"
