from rest_framework import generics, status

from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView

from rest_framework.response import Response
from chat_room.models import ChatRoom, Message
from chat_room.serializers import ChatRoomSerializer, MessageSerializer
from chat_room.api.permissions import IsMessageUserOrReadOnly

from users.models import Account


class ChatRoomCreate(generics.CreateAPIView):
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAdminUser]


class ChatRoomsList(generics.ListAPIView):
    serializer_class = ChatRoomSerializer

    def get_queryset(self):
        return ChatRoom.objects.all()


class MessageList(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.all()


class RoomsMessageList(generics.ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        number = self.kwargs.get('pk')
        return Message.objects.filter(room__id=number)


class MessageCreate(generics.CreateAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        room = ChatRoom.objects.get(pk=pk)
        if isinstance(self.request.user, Account):
            message_author = self.request.user
        # else:
        #     message_author = Account.objects.get(id=56)
        #     message_author = None
        room.posts_quantity = room.posts_quantity + 1
        room.save()
        serializer.save(room=room, message_author=message_author)


class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    permission_classes = [IsMessageUserOrReadOnly]

    def delete(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        room = ChatRoom.objects.get(message__id__exact=pk)
        room.posts_quantity = room.posts_quantity - 1
        room.save()
        return self.destroy(request, *args, **kwargs)


class LikeMessage(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        message = Message.objects.get(pk=pk)
        message.liked += 1
        message.save()
        return Response(status=status.HTTP_200_OK)


class DisLikeMessage(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        message = Message.objects.get(pk=pk)
        message.liked -= 1
        message.save()
        return Response(status=status.HTTP_200_OK)

