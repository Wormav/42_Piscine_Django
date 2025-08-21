from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import CustomUser as User
from .models import Tip


class TipForm(forms.ModelForm):
    class Meta:
        model = Tip
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Share your life pro tip here! (max 500 characters)",
                    "rows": 3,
                    "maxlength": 500,
                }
            )
        }
        labels = {"content": ""}


class SignupForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, required=True)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)


def home(request):
    tips = Tip.objects.all()
    tip_form = None

    if request.user.is_authenticated:
        if request.method == "POST":
            tip_form = TipForm(request.POST)
            if tip_form.is_valid():
                tip = tip_form.save(commit=False)
                tip.author = request.user
                tip.save()
                return redirect("home")
        else:
            tip_form = TipForm()

    return render(request, "home.html", {"tips": tips, "tip_form": tip_form})


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


@login_required
def upvote_tip(request, tip_id):
    tip = get_object_or_404(Tip, id=tip_id)
    user = request.user

    if tip.upvotes.filter(id=user.id).exists():
        tip.upvotes.remove(user)
    else:
        if tip.downvotes.filter(id=user.id).exists():
            tip.downvotes.remove(user)
        tip.upvotes.add(user)

    return redirect("home")


@login_required
def downvote_tip(request, tip_id):
    tip = get_object_or_404(Tip, id=tip_id)
    user = request.user

    if tip.downvotes.filter(id=user.id).exists():
        tip.downvotes.remove(user)
    else:
        if tip.upvotes.filter(id=user.id).exists():
            tip.upvotes.remove(user)

        tip.downvotes.add(user)

    return redirect("home")


@login_required
def delete_tip(request, tip_id):
    tip = get_object_or_404(Tip, id=tip_id)

    if request.user != tip.author:
        return redirect("home")

    tip.delete()
    return redirect("home")
