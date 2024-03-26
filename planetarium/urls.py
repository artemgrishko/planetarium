from django.urls import path, include
from rest_framework import routers

from .views import ShowThemeViewSet

router = routers.DefaultRouter()

router.register("show_themes", ShowThemeViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "planetarium"
