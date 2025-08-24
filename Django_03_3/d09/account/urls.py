from django.urls import path

from . import views

app_name = "account"

urlpatterns = [
    path("", views.account_view, name="account"),
    path("signin/", views.signin_view, name="signin"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_ajax, name="login_ajax"),
    path("signup-ajax/", views.signup_ajax, name="signup_ajax"),
    path("logout/", views.logout_ajax, name="logout_ajax"),
    path("status/", views.get_user_status, name="user_status"),
]
