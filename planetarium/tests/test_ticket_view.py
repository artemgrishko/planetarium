from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


TICKET_URL = reverse("planetarium:ticket-list")


class UnauthenticatedTicketViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(TICKET_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedTicketTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.test",
            password="test_password"
        )
        self.client.force_authenticate(self.user)

    def test_ticket_list_access(self):
        res = self.client.get(TICKET_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
