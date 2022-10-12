from rest_framework import serializers
from chat_room.models import ChatRoom, Message


class ChatRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatRoom
        fields = "__all__"
        posts_quantity = len(ChatRoom.objects.all())
        print(posts_quantity)
        extra_kwargs = {
            'posts_quantity': {'read_only': True}
        }


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = "__all__"
        extra_kwargs = {
            'room': {'read_only': True},
            'message_author': {'required': False, 'read_only': True}
        }