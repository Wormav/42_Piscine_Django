from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class ChatRoom(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Message(models.Model):
    MESSAGE_TYPES = [
        ("message", "Message"),
        ("user_joined", "User Joined"),
        ("user_left", "User Left"),
    ]

    room = models.ForeignKey(
        ChatRoom, on_delete=models.CASCADE, related_name="messages"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    message_type = models.CharField(
        max_length=20, choices=MESSAGE_TYPES, default="message"
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return f"{self.user.username}: {self.content[:50]}"
        return f"System: {self.content[:50]}"

    class Meta:
        ordering = ["timestamp"]
