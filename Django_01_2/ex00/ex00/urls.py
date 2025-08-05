from django.urls import path
from . import views

urlpatterns = [
    path('', views.markdown_cheatsheet, name='markdown_cheatsheet'),
]
