import random
import time

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render


def home(request):
    username = request.session.get("anon_username")
    timestamp = request.session.get("anon_timestamp")
    now = int(time.time())

    if not username or not timestamp or now - timestamp > 42:
        username = random.choice(settings.ANONYMOUS_USERNAMES)
        request.session["anon_username"] = username
        request.session["anon_timestamp"] = now

    return render(request, "home.html", {"username": username})


def get_username(request):
    username = request.session.get("anon_username")
    timestamp = request.session.get("anon_timestamp")
    now = int(time.time())

    if not username or not timestamp or now - timestamp > 42:
        username = random.choice(settings.ANONYMOUS_USERNAMES)
        request.session["anon_username"] = username
        request.session["anon_timestamp"] = now

    return JsonResponse({"username": username})
