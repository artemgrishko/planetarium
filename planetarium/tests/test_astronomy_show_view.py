from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from planetarium.models import AstronomyShow, ShowTheme
from planetarium.serializers import AstronomyShowListSerializer, AstronomyShowDetailSerializer

AstronomyShow_URL = reverse("planetarium:astronomyshow-list")


def sample_show(**params):
    default = {
        "title": "Test",
        "description": "test description",
    }
    default.update(params)

    return AstronomyShow.objects.create(**default)


def detail_url(show_id):
    return reverse("planetarium:astronomyshow-list", args=(show_id,))


class UnauthenticatedShowThemeViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(AstronomyShow_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAstronomyShowTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.test",
            password="test_password"
        )
        self.client.force_authenticate(self.user)

    def test_astronomy_show_list_access(self):
        sample_show()

        res = self.client.get(AstronomyShow_URL)

        movies = AstronomyShow.objects.all()
        serializer = AstronomyShowListSerializer(movies, many=True)

        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    # def test_filter_movies_by_title(self):
    #     movie_with_title1 = sample_show()
    #     movie_with_title2 = sample_show(title="Test2")
    #
    #     res = self.client.get(
    #         AstronomyShow_URL,
    #         {"title": movie_with_title1.title}
    #     )
    #
    #     serializer_with_show_title1 = AstronomyShowListSerializer(movie_with_title1)
    #     serializer_with_show_title2 = AstronomyShowListSerializer(movie_with_title2)
    #
    #     self.assertIn(serializer_with_show_title1.data, res.data)
    #     self.assertNotIn(serializer_with_show_title2.data, res.data)
    def test_filter_shows_by_show_theme_ids(self):
        show_with_show_theme = sample_show()
        show_without_show_theme = sample_show(title="Test2")

        show_theme = ShowTheme.objects.create(name="First")

        show_with_show_theme.show_theme.add(show_theme)

        res = self.client.get(
            AstronomyShow_URL,
            {"show_theme": show_theme.id}
        )

        serializer_with_show_theme = AstronomyShowListSerializer(show_with_show_theme)
        serializer_without_show_theme = AstronomyShowListSerializer(show_without_show_theme)

        self.assertIn(serializer_with_show_theme.data, res.data)
        self.assertNotIn(serializer_without_show_theme.data, res.data)

    # def test_retrieve_show_detail(self):
    #     show = sample_show()
    #     show_theme = ShowTheme.objects.create(name="First")
    #
    #     show.show_theme.add(show_theme)
    #
    #     url = detail_url(show.id)
    #
    #     res = self.client.get(url)
    #
    #     serializer = AstronomyShowDetailSerializer(show)
    #
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(res.data, serializer.data)

    def test_create_forbidden(self):
        payload = {
            "title": "TEST",
            "description": "test description",
        }

        res = self.client.post(AstronomyShow_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminMovieViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@admin.admin",
            password="test_password",
            is_staff=True,
        )
        self.client.force_authenticate(self.user)

    def test_create_show(self):
        payload = {
            "title": "Test",
            "description": "test description",
        }

        res = self.client.post(AstronomyShow_URL, payload)

        movie = AstronomyShow.objects.get(id=res.data["id"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        for key in payload:
            self.assertEqual(payload[key], getattr(movie, key))

    def test_create_show_with_show_theme(self):
        show_theme = ShowTheme.objects.create(name="First")

        payload = {
            "title": "Test",
            "description": "test description",
            "show_theme": [show_theme.id],
        }

        res = self.client.post(AstronomyShow_URL, payload)

        show_themes = ShowTheme.objects.all()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn(show_theme, show_themes)
