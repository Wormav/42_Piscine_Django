from django.urls import path

from .views import (
    ArticleCreateView,
    ArticleDeleteView,
    ArticleDetailView,
    ArticleListView,
    CustomLoginView,
    CustomLogoutView,
    HomeView,
    SignUpView,
    ToggleFavouriteView,
    UserFavouritesView,
    UserPublicationsView,
)

app_name = "articles"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("articles/", ArticleListView.as_view(), name="list"),
    path("articles/<int:pk>/", ArticleDetailView.as_view(), name="detail"),
    path(
        "articles/<int:pk>/toggle-favourite/",
        ToggleFavouriteView.as_view(),
        name="toggle_favourite",
    ),
    path("create/", ArticleCreateView.as_view(), name="create"),
    path("articles/<int:pk>/delete/", ArticleDeleteView.as_view(), name="delete"),
    path("publications/", UserPublicationsView.as_view(), name="publications"),
    path("favourites/", UserFavouritesView.as_view(), name="favourites"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
]
