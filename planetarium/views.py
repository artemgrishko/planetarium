from datetime import datetime

from django.db.models import F, Count
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from planetarium.models import (
    ShowTheme,
    AstronomyShow,
    PlanetariumDome,
    ShowSession,
    Ticket,
    Reservation
)
from planetarium.permissions import IsAdminOrIfAuthenticatedReadOnly
from planetarium.serializers import (
    ShowThemeSerializer,
    AstronomyShowSerializer,
    PlanetariumDomeSerializer,
    ShowSessionSerializer,
    TicketSerializer,
    AstronomyShowDetailSerializer,
    ShowSessionDetailSerializer,
    ReservationSerializer,
    TicketDetailSerializer,
    TicketListSerializer,
    AstronomyShowListSerializer,
    ReservationDetailSerializer,
    ShowSessionListSerializer,
    AstronomyShowImageSerializer,
)


class OrderPagination(PageNumberPagination):
    page_size = 5
    max_page_size = 50


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class AstronomyShowViewSet(viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.all()
    serializer_class = AstronomyShowSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AstronomyShowDetailSerializer
        if self.action == "list":
            return AstronomyShowListSerializer
        return self.serializer_class

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
    )
    def upload_image(self, request, pk=None):
        """Endpoint for uploading image to specific movie"""
        astronomy_show = self.get_object()
        serializer = AstronomyShowImageSerializer(astronomy_show, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        """Retrieve the movies with filters"""
        title = self.request.query_params.get("title")
        show_theme = self.request.query_params.get("show_theme")

        queryset = self.queryset

        if title:
            queryset = queryset.filter(title__icontains=title)

        if show_theme:
            show_theme_ids = self._params_to_ints(show_theme)
            queryset = queryset.filter(show_theme__id__in=show_theme_ids)

        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "show_theme",
                type={"type": "array", "items": {"type": "number"}},
                description="Filter by show themes id",
            ),
            OpenApiParameter("title", type=str, description="Filter by title"),
        ]
    )
    def list(self, request, *args, **kwargs):
        """Get list of show astronomy shows"""
        return super().list(request, *args, **kwargs)


class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = ShowSession.objects.all().annotate(
        tickets_available=(
            F("planetarium_dome__rows")) * F("planetarium_dome__seats_in_row") - Count("tickets"))
    serializer_class = ShowSessionSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return ShowSessionListSerializer
        if self.action == "retrieve":
            return ShowSessionDetailSerializer
        return self.serializer_class

    def get_queryset(self):
        show_time = self.request.query_params.get("show_time")
        astronomy_show = self.request.query_params.get("astronomy_show")

        queryset = self.queryset

        if show_time:
            time = datetime.strptime(datetime.date, "%Y-%m-%d").date()
            queryset = queryset.filter(show_time=time)

        if astronomy_show:
            queryset = queryset.filter(astronomy_show_id=int(astronomy_show))

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "show_time",
                type=str,
                description="Filter by show_time",
            ),
            OpenApiParameter(
                "astronomy_show",
                type=int,
                description="Filter by astronomy_show id",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        """Get list of show sessions"""
        return super().list(request, *args, **kwargs)


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    pagination_class = OrderPagination
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return TicketDetailSerializer
        if self.action == "list":
            return TicketListSerializer
        return self.serializer_class


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ReservationDetailSerializer
        return self.serializer_class

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
