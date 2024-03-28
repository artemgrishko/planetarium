from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from planetarium.models import (
    ShowTheme,
    AstronomyShow,
    Reservation,
    PlanetariumDome,
    ShowSession,
    Ticket
)
from user.serializers import UserSerializer


class ShowThemeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShowTheme
        fields = ("id", "name",)


class AstronomyShowSerializer(serializers.ModelSerializer):

    class Meta:
        model = AstronomyShow
        fields = ("id", "title", "description", "show_theme",)


class AstronomyShowListSerializer(AstronomyShowSerializer):
    show_theme = serializers.SerializerMethodField()

    class Meta:
        model = AstronomyShow
        fields = ("id", "title", "description", "show_theme", "image")

    def get_show_theme(self, obj):
        return [theme.name for theme in obj.show_theme.all()]


class AstronomyShowImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AstronomyShow
        fields = ("id", "image")


class AstronomyShowDetailSerializer(AstronomyShowSerializer):
    show_theme = ShowThemeSerializer(many=True, read_only=True)
    image = AstronomyShowImageSerializer(read_only=True)

    class Meta:
        model = AstronomyShow
        fields = ("id", "title", "description", "show_theme", "image")


class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = ("id", "created_at",)


class ReservationDetailSerializer(ReservationSerializer):
    user = UserSerializer(read_only=True)


class PlanetariumDomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlanetariumDome
        fields = ("id", "name", "rows", "seats_in_row", "capacity",)


class ShowSessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShowSession
        fields = ("id", "astronomy_show", "planetarium_dome", "show_time",)


class ShowSessionDetailSerializer(ShowSessionSerializer):
    astronomy_show = AstronomyShowDetailSerializer()
    planetarium_dome = PlanetariumDomeSerializer()


class ShowSessionListSerializer(ShowSessionSerializer):
    astronomy_show = AstronomyShowListSerializer()
    tickets_available = serializers.IntegerField(read_only=True)
    planetarium_dome_name = serializers.CharField(
        read_only=True,
        source="planetarium_dome.name"
    )
    planetarium_dome_capacity = serializers.IntegerField(
        read_only=True,
        source="planetarium_dome.capacity"
    )

    class Meta:
        model = ShowSession
        fields = (
            "id",
            "astronomy_show",
            "planetarium_dome_name",
            "planetarium_dome_capacity",
            "show_time",
            "tickets_available",
        )


class TicketSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs=attrs)
        Ticket.validate_ticket(
            attrs["row"],
            attrs["seat"],
            attrs["show_session"].planetarium_dome,
            ValidationError,
        )
        return data

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "show_session", "reservation",)


class TicketDetailSerializer(TicketSerializer):
    show_session = ShowSessionDetailSerializer(many=False, read_only=True)
    reservation = ReservationSerializer(many=False, read_only=True)


class TicketListSerializer(TicketSerializer):
    show_session = ShowSessionListSerializer(many=False, read_only=True)
