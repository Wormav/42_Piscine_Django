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
    upvotes = models.ManyToManyField(
        CustomUser, related_name="upvoted_tips", blank=True
    )
    downvotes = models.ManyToManyField(
        CustomUser, related_name="downvoted_tips", blank=True
    )

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.author.username}: {self.content[:50]}..."

    def upvote_count(self):
        return self.upvotes.count()

    def downvote_count(self):
        return self.downvotes.count()

    def net_votes(self):
        return self.upvote_count() - self.downvote_count()

    def user_vote_status(self, user):
        if user.is_anonymous:
            return None
        if self.upvotes.filter(id=user.id).exists():
            return "upvote"
        elif self.downvotes.filter(id=user.id).exists():
            return "downvote"
        return None
