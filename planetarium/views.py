from rest_framework import mixins, viewsets
from rest_framework.viewsets import GenericViewSet

from planetarium.models import ShowTheme, AstronomyShow, PlanetariumDome, ShowSession, Ticket
from planetarium.serializers import ShowThemeSerializer, AstronomyShowSerializer, PlanetariumDomeSerializer, \
    ShowSessionSerializer, TicketSerializer, AstronomyShowDetailSerializer


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer


class AstronomyShowViewSet(viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.all()
    serializer_class = AstronomyShowSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AstronomyShowDetailSerializer
        return self.serializer_class


class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = ShowSession.objects.all()
    serializer_class = ShowSessionSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer



