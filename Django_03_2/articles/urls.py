from django.urls import path

from .views import (
    ArticleListView,
    CustomLoginView,
    CustomLogoutView,
    HomeView,
    SignUpView,
)

app_name = "articles"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("articles/", ArticleListView.as_view(), name="list"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
]
