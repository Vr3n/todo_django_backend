from django.urls import reverse_lazy
from rest_framework.test import APITestCase
from rest_framework import status

# Create your tests here.


class RegisterUserTest(APITestCase):

    def setUp(self):
        self.valid_payload = {
            "username": "virus",
            "email": "vicky@gmail.com",
            "mobile_number": "1234567890",
            "password": "Django@123",
            "password2": "Django@123"
        }

        self.invalid_payload = {
            "username": "virus",
            "email": "vicky@gmail.com",
            "mobile_number": "1234567890",
            "password1": "Django@123",
            "password2": "Django@123"
        }

    def test_register_user(self):
        response = self.client.post(reverse_lazy('api_register_user'),
                                    self.valid_payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
