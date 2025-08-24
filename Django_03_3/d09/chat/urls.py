from django.urls import path

from . import views

app_name = "chat"

urlpatterns = [
    path("", views.chat_home, name="home"),
    path("home/", views.chat_home, name="chat_home"),
    path("room/<str:room_name>/", views.chatroom, name="chatroom"),
]
