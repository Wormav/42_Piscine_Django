from django.contrib import admin

from .models import ChatRoom, Message


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["name"]
    ordering = ["name"]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["room", "user", "message_type", "content", "timestamp"]
    list_filter = ["message_type", "timestamp", "room"]
    search_fields = ["content", "user__username"]
    ordering = ["-timestamp"]
    readonly_fields = ["timestamp"]
