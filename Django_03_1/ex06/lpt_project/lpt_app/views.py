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

    for tip in tips:
        tip.can_delete = request.user.is_authenticated and (  # type: ignore
            request.user == tip.author
            or request.user.is_superuser
            or request.user.has_perm("lpt_app.delete_tip")
        )

        tip.can_downvote = request.user.is_authenticated and (  # type: ignore
            request.user.is_superuser
            or request.user == tip.author
            or (
                request.user != tip.author
                and request.user.has_perm("lpt_app.can_downvote_tips")
            )
        )

    user_has_delete_perm = request.user.is_authenticated and request.user.has_perm(
        "lpt_app.delete_tip"
    )

    user_has_downvote_perm = request.user.is_authenticated and request.user.has_perm(
        "lpt_app.can_downvote_tips"
    )

    context = {
        "tips": tips,
        "tip_form": tip_form,
        "user_has_delete_perm": user_has_delete_perm,
        "user_has_downvote_perm": user_has_downvote_perm,
    }

    return render(request, "home.html", context)


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

    # New rule: users with can_downvote_tips permission can only downvote others' tips
    # Superusers and authors can still downvote their own tips
    can_downvote = (
        user.is_superuser  # Superuser can downvote anything
        or (user == tip.author)  # Author can downvote their own tip
        or (
            user != tip.author and user.has_perm("lpt_app.can_downvote_tips")
        )  # Others only with permission
    )

    if not can_downvote:
        return redirect("home")

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

    # Deletion permission checks:
    # 1. The user is the author of the tip (always allowed)
    # 2. The user is a superuser (can delete anything)
    # 3. The user has the special 'delete_tip' permission
    can_delete = (
        request.user == tip.author
        or request.user.is_superuser
        or request.user.has_perm("lpt_app.delete_tip")
    )

    if not can_delete:
        return redirect("home")

    tip.delete()
    return redirect("home")
