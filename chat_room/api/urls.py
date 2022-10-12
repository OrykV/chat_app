from django.urls import path
from chat_room.api import views

urlpatterns = [
    path('room-create/', views.ChatRoomCreate.as_view(), name='room-create'),
    path('list/', views.ChatRoomsList.as_view(), name='room-list'),

    path('<int:pk>/message-create/', views.MessageCreate.as_view(), name='message-create'),
    path('<int:pk>/messages/', views.RoomsMessageList.as_view(), name='rooms-message-list'),
    path('message/<int:pk>/', views.MessageDetail.as_view(), name='message-detail'),
    path('message/<int:pk>/like', views.LikeMessage.as_view(), name='message-like'),
    path('message/<int:pk>/dislike', views.DisLikeMessage.as_view(), name='message-dislike'),
    path('messages/', views.MessageList.as_view(), name='message-list'),
]

