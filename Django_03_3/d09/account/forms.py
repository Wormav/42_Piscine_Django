from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Custom registration form for CustomUser.
    """

    class Meta:
        model = CustomUser
        fields = ("username", "password1", "password2")
