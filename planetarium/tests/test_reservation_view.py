from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


RESERVATION_URL = reverse("planetarium:reservation-list")


class UnauthenticatedReservationView(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(RESERVATION_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedReservationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.test",
            password="test_password"
        )
        self.client.force_authenticate(self.user)

    def test_reservation_list_access(self):
        res = self.client.get(RESERVATION_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
