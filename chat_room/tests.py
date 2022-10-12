from django.test import TestCase
from django.urls import reverse
from users.models import Account

from chat_room.models import Message, ChatRoom

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from chat_room import models


class ChatRoomTestCase(APITestCase):

    def setUp(self):
        self.user = Account.objects.create_user(username="api9@gmail.com",
                                                password="useruser",
                                                first_name="Bob",
                                                last_name="Marley",
                                                email="api9@gmail.com")
        self.client.post(reverse('login'), {"username": "api9@gmail.com", "password": "useruser"})
        self.token = Token.objects.get(user__username="api9@gmail.com")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        # self.room = models.ChatRoom.objects.create(name = "Test")

    def test_chatroom_create(self):
        data = {
            "name": "New room"
        }
        response = self.client.post(reverse('room-create'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_chatroom_list(self):
        response = self.client.get(reverse('room-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MessageTestCase(APITestCase):
    def setUp(self):
        self.user = Account.objects.create_user(username="api9@gmail.com",
                                                password="useruser",
                                                first_name="Bob",
                                                last_name="Marley",
                                                email="api9@gmail.com")
        self.client.post(reverse('login'), {"username": "api9@gmail.com", "password": "useruser"})
        self.token = Token.objects.get(user__username="api9@gmail.com")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.room = models.ChatRoom.objects.create(name = "Test")

    def create_another_user(self):
        self.user = Account.objects.create_user(username="api1@gmail.com",
                                                password="useruser",
                                                first_name="Jack",
                                                last_name="Barley",
                                                email="api1@gmail.com")
        self.client.post(reverse('login'), {"username": "api1@gmail.com", "password": "useruser"})
        self.token = Token.objects.get(user__username="api1@gmail.com")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_message_create(self):
        data = {"text": "New message!"}
        response = self.client.post(reverse('message-create', args=(self.room.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_message_list(self):
        response = self.client.get(reverse('message-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_rooms_message_list(self):
        response = self.client.get(reverse('rooms-message-list', args=(self.room.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_message_update(self):
        self.test_message_create()
        data = {"text": "Message updated!"}
        response = self.client.put(reverse('message-detail', args=(1,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_message_delete(self):
        self.test_message_create()
        response = self.client.delete(reverse('message-detail', args=(1,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_message_update_another_user(self):
        self.test_message_create()
        self.create_another_user()
        data = {"text": "Updated by another user!"}
        response = self.client.put(reverse('message-detail', args=(1,)), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_message_delete_another_user(self):
        self.test_message_create()
        self.create_another_user()
        response = self.client.delete(reverse('message-detail', args=(1,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_like(self):
        self.test_message_create()
        response = self.client.put(reverse('message-like', args=(1,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_dislike(self):
        self.test_message_create()
        response = self.client.put(reverse('message-dislike', args=(1,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)