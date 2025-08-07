from django.urls import path
from . import views

urlpatterns = [
    path('', views.color_shades, name='color_shades'),
]
