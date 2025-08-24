from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import ChatRoom


def home(request):
    """
    Vue pour la page d'accueil - redirige selon l'authentification
    """
    if request.user.is_authenticated:
        return redirect("chat:chat_home")
    else:
        return redirect("account:signin")


@login_required
def chat_home(request):
    """
    Vue pour la page d'accueil du chat - accessible uniquement aux utilisateurs connectés
    """
    chatrooms = ChatRoom.objects.all()
    return render(request, "chat/home.html", {"chatrooms": chatrooms})


@login_required
def chatroom(request, room_name):
    """
    Vue pour une chatroom spécifique
    """
    try:
        room = ChatRoom.objects.get(name=room_name)
        return render(request, "chat/chatroom.html", {"room": room})
    except ChatRoom.DoesNotExist:
        return redirect("chat:home")
