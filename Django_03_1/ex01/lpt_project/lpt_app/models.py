# Create your models here.
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    # Ajoute ici des champs personnalisés si besoin
    pass
