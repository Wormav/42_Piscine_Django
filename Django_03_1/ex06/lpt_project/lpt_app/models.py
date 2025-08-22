# Create your models here.
from django.contrib.auth.models import AbstractUser, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import m2m_changed, post_delete
from django.dispatch import receiver
from django.utils import timezone


class CustomUser(AbstractUser):
    def calculate_reputation(self):
        """Calculate user's reputation based on votes received on their tips"""
        reputation = 0
        for tip in self.tips.all():  # type: ignore
            reputation += tip.upvote_count() * 5  # +5 per upvote
            reputation -= tip.downvote_count() * 2  # -2 per downvote
        return reputation

    def update_permissions(self):
        """Update user permissions based on reputation thresholds"""
        reputation = self.calculate_reputation()

        # Get the content type for Tip model
        tip_content_type = ContentType.objects.get(app_label="lpt_app", model="tip")

        # Get the permissions
        try:
            downvote_permission = Permission.objects.get(
                codename="can_downvote_tips", content_type=tip_content_type
            )
            delete_permission = Permission.objects.get(
                codename="delete_tip", content_type=tip_content_type
            )
        except Permission.DoesNotExist:
            # Permissions don't exist yet (probably during migrations)
            return

        # Manage downvote permission (15+ points)
        if reputation >= 15:
            if not self.has_perm("lpt_app.can_downvote_tips"):
                self.user_permissions.add(downvote_permission)
        else:
            if self.has_perm("lpt_app.can_downvote_tips") and not self.is_superuser:
                self.user_permissions.remove(downvote_permission)

        # Manage delete permission (30+ points)
        if reputation >= 30:
            if not self.has_perm("lpt_app.delete_tip"):
                self.user_permissions.add(delete_permission)
        else:
            if self.has_perm("lpt_app.delete_tip") and not self.is_superuser:
                self.user_permissions.remove(delete_permission)

    @property
    def reputation(self):
        """Property to easily access reputation in templates"""
        return self.calculate_reputation()

    def can_downvote_others_tips(self):
        """Check if user can downvote tips from other users"""
        return self.is_superuser or self.has_perm("lpt_app.can_downvote_tips")

    def can_delete_tips(self):
        """Check if user can delete tips"""
        return self.is_superuser or self.has_perm("lpt_app.delete_tip")


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
        permissions = [
            ("can_downvote_tips", "Can downvote any tip"),
        ]

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


# Signals to automatically update user permissions when votes change
@receiver(m2m_changed, sender=Tip.upvotes.through)
@receiver(m2m_changed, sender=Tip.downvotes.through)
def update_user_permissions_on_vote_change(sender, instance, action, pk_set, **kwargs):
    """Update permissions when votes are added or removed"""
    if action in ["post_add", "post_remove"]:
        # Update permissions for the tip's author
        instance.author.update_permissions()


@receiver(post_delete, sender=Tip)
def update_user_permissions_on_tip_delete(sender, instance, **kwargs):
    """Update permissions when a tip is deleted"""
    instance.author.update_permissions()
