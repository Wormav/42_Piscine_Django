from django import forms
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .models import CustomUser as User


class SignupForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, required=True)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)


def home(request):
    return render(request, "home.html")


def signup(request):
    if request.user.is_authenticated:
        return redirect("home")
    errors = []
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password1 = form.cleaned_data["password1"]
            password2 = form.cleaned_data["password2"]
            if User.objects.filter(username=username).exists():
                errors.append("Username already exists.")
            elif password1 != password2:
                errors.append("Passwords do not match.")
            else:
                user = User.objects.create_user(username=username, password=password1)
                login(request, user)
                return redirect("home")
        else:
            errors.append("All fields are required.")
    else:
        form = SignupForm()
    return render(request, "signup.html", {"form": form, "errors": errors})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    errors = []
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                errors.append("Invalid credentials.")
        else:
            errors.append("All fields are required.")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form, "errors": errors})


def logout_view(request):
    logout(request)
    return redirect("home")
