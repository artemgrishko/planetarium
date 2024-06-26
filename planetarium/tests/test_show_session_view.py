from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


SHOW_SESSION_URL = reverse("planetarium:showsession-list")


class UnauthenticatedShowSessionView(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(SHOW_SESSION_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedShowSessionTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.test",
            password="test_password"
        )
        self.client.force_authenticate(self.user)

    def test_show_session_list_access(self):
        res = self.client.get(SHOW_SESSION_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
