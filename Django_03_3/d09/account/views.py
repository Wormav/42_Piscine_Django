import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_POST


def signin_view(request):
    """
    Vue pour la page de signin.
    """
    if request.user.is_authenticated:
        return redirect("chat:home")
    return render(request, "account/signin.html")


def signup_view(request):
    """
    View for the signup page.
    """
    if request.user.is_authenticated:
        return redirect("chat:home")
    return render(request, "account/signup.html")


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
def signup_ajax(request):
    """
    AJAX endpoint for user signup.
    """
    try:
        data = json.loads(request.body)
        username = data.get("username")
        password1 = data.get("password1")
        password2 = data.get("password2")

        # Manual validation
        errors = {}

        if not username:
            errors["username"] = ["This field is required."]
        elif len(username) < 3:
            errors["username"] = ["Username must contain at least 3 characters."]

        if not password1:
            errors["password1"] = ["This field is required."]
        elif len(password1) < 8:
            errors["password1"] = ["Password must contain at least 8 characters."]

        if not password2:
            errors["password2"] = ["This field is required."]
        elif password1 != password2:
            errors["password2"] = ["The two passwords do not match."]

        # Check if user already exists
        from .models import CustomUser

        if username and CustomUser.objects.filter(username=username).exists():
            errors["username"] = ["A user with this username already exists."]

        if errors:
            return JsonResponse({"success": False, "errors": errors})

        # Create the user
        user = CustomUser.objects.create_user(username=username, password=password1)

        # Log in the user
        login(request, user)
        return JsonResponse({"success": True, "username": user.username})

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
