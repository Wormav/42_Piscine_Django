from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    This allows for future customizations if needed.
    """

    pass
