from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    Formulaire d'inscription personnalisé pour CustomUser.
    """

    class Meta:
        model = CustomUser
        fields = ("username", "password1", "password2")
