# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    pass


class Tip(models.Model):
    content = models.TextField(max_length=500, help_text="Share your life pro tip!")
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="tips"
    )
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.author.username}: {self.content[:50]}..."
