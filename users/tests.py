from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
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

        self.invalid_email = {
            "username": "virus",
            "email": "vicky.com",
            "mobile_number": "1234567890",
            "password1": "Django@123",
            "password2": "Django@123"
        }

        self.mobile_number_already_exists = {
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

    def test_invalid_payload(self):
        response = self.client.post(reverse_lazy(
            'api_register_user'), self.invalid_payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_email(self):
        response = self.client.post(reverse_lazy(
            'api_register_user'), self.invalid_email)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_mobile_number_already_exists(self):

        get_user_model().objects.create(
            username=self.mobile_number_already_exists['username'],
            email=self.mobile_number_already_exists['email'],
            mobile_number=self.mobile_number_already_exists['mobile_number']
        )

        response = self.client.post(reverse_lazy(
            'api_register_user'), self.invalid_email)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
