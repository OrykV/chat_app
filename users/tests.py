from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.urls import reverse
from rest_framework import status
from users.models import Account


class RegisterTestCase(APITestCase):

    def test_register(self):
        data = {
            "username": "testcase",
            "email": "testcase@example.com",
            "password": "NewPassword@123",
            "password2": "NewPassword@123"
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginLogoutTestCase(APITestCase):

    def setUp(self):
        self.user = Account.objects.create_user(username="api9@gmail.com",
                                                password="useruser",
                                                first_name="Bob",
                                                last_name="Marley",
                                                email="api9@gmail.com")

    def test_login(self):
        response = self.client.post(reverse('login'), {"username": "api9@gmail.com", "password": "useruser"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        self.client.post(reverse('login'), {"username": "api9@gmail.com", "password": "useruser"})
        self.token = Token.objects.get(user__username="api9@gmail.com")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)