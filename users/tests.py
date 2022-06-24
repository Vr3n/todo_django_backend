from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from .models import Profile

# Create your tests here.


class RegisterUserTest(APITestCase):

    def setUp(self):
        self.valid_payload = {
            'first_name': 'test',
            'last_name': 'tset',
            "username": "virus",
            "email": "vicky@gmail.com",
            "mobile_number": "1234567890",
            "password": "Django@123",
            "password2": "Django@123"
        }

        self.invalid_payload = {
            'first_name': 'test',
            'last_name': 'tset',
            "username": "virus",
            "email": "vicky@gmail.com",
            "mobile_number": "1234567890",
            "password1": "Django@123",
            "password2": "Django@123"
        }

        self.invalid_email = {
            'first_name': 'test',
            'last_name': 'tset',
            "username": "virus",
            "email": "vicky.com",
            "mobile_number": "1234567890",
            "password1": "Django@123",
            "password2": "Django@123"
        }

        self.mobile_number_already_exists = {
            'first_name': 'test',
            'last_name': 'tset',
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

    def test_token_created_after_user_registers(self):
        """Testing the Creation of auth token after the user registers.

        Check if the Signals are creating the Tokens after the user registers.
        """

        User = get_user_model()

        self.client.post(reverse_lazy('api_register_user'),
                         self.valid_payload)

        # user = User(username=self.valid_payload['username'],
        #             email=self.valid_payload['email'],
        #             mobile_number=self.valid_payload['mobile_number'],
        #             first_name="test",
        #             last_name="tset")

        user = User.objects.get(email=self.valid_payload)

        user.save()

        token_obj = Token.objects.get(user=user)

        self.assertEqual(user.email, token_obj.user.email)

    def test_profile_created_after_user_registered(self):
        """Testing the Creation of Profile after the user registers.

        Check if the Signals are creating the Profile after the user registers.
        """

        User = get_user_model()

        self.client.post(reverse_lazy('api_register_user'),
                         self.valid_payload)

        # user = User(username=self.valid_payload['username'],
        #             email=self.valid_payload['email'],
        #             mobile_number=self.valid_payload['mobile_number'],
        #             first_name="test",
        #             last_name="tset")

        user = User.objects.get(email=self.valid_payload)

        profile_obj = Profile.objects.get(user=user)

        self.assertEqual(user.email, profile_obj.user.email)
        self.assertEqual(f'{user.email} - Profile', str(profile_obj))


class ProfileAPITestCase(APITestCase):

    def setUp(self):
        self.user = {
            'first_name': 'test',
            'last_name': 'tset',
            "username": "virus",
            "email": "vicky@gmail.com",
            "mobile_number": "1234567890",
            "password": "Django@123",
            "password2": "Django@123"
        }
        self.other_user = {
            'first_name': 'test',
            'last_name': 'tset',
            "username": "virup",
            "email": "vicky@gmail.com",
            "mobile_number": "1234567898",
            "password": "Django@123",
            "password2": "Django@123"
        }

        self.profile = {
            'about': 'This is test about!'
        }

    def test_forbidden_when_updating_other_user(self):
        user = get_user_model().objects.create(
            username=self.user['username'],
            email=self.user['email'],
            mobile_number=self.user['mobile_number'],
            first_name=self.user['first_name'],
            last_name=self.user['last_name'],
        )

        other_user = get_user_model().objects.create(
            username=self.other_user['username'],
            email=self.other_user['email'],
            mobile_number=self.other_user['mobile_number'],
            first_name=self.other_user['first_name'],
            last_name=self.other_user['last_name'],
        )

        self.client.force_login(user)

        profile = Profile.objects.get(user=other_user)

        self.profile['user'] = other_user.id

        res = self.client.put(
            reverse_lazy('api_profile', kwargs={'pk': profile.id}),
            data=self.profile)

        self.assertEqual(status.HTTP_403_FORBIDDEN, res.status_code)
        self.assertEqual({"error": 'You cannot update this profile!'},
                         res.json())
