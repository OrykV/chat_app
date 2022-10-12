from django.db import models
from users.models import Account


class ChatRoom(models.Model):
    name = models.CharField(max_length=30, null=False)
    posts_quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Message(models.Model):
    message_author = models.ForeignKey(Account, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    liked = models.IntegerField(default=0)

    def __str__(self):
        return self.text