import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_POST


@ensure_csrf_cookie
def account_view(request):
    """
    Main account view that displays login form or logged in status.
    """
    return render(request, "account/account.html")


@csrf_exempt
@require_POST
def login_ajax(request):
    """
    AJAX endpoint for user login.
    """
    try:
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        form = AuthenticationForm(data={"username": username, "password": password})

        if form.is_valid():
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({"success": True, "username": user.username})

        # Return form errors
        return JsonResponse({"success": False, "errors": form.errors})

    except json.JSONDecodeError:
        return JsonResponse(
            {"success": False, "errors": {"__all__": ["Invalid JSON data"]}}
        )


@csrf_exempt
@require_POST
def logout_ajax(request):
    """
    AJAX endpoint for user logout.
    """
    logout(request)
    return JsonResponse({"success": True})


def get_user_status(request):
    """
    AJAX endpoint to get current user status.
    """
    if request.user.is_authenticated:
        return JsonResponse({"authenticated": True, "username": request.user.username})
    else:
        return JsonResponse({"authenticated": False, "csrf_token": get_token(request)})
