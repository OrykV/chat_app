from django.contrib import admin
from chat_room import models


class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "posts_quantity")


class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "room", "liked", "message_author")


admin.site.register(models.ChatRoom, ChatRoomAdmin)
admin.site.register(models.Message, MessageAdmin)