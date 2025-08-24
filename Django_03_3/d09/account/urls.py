from django.urls import path

from . import views

app_name = "account"

urlpatterns = [
    path("", views.account_view, name="account"),
    path("login/", views.login_ajax, name="login_ajax"),
    path("logout/", views.logout_ajax, name="logout_ajax"),
    path("status/", views.get_user_status, name="user_status"),
]
