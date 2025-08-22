from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, RedirectView, View

from .forms import ArticleForm
from .models import Article, UserFavouriteArticle


class HomeView(RedirectView):
    """Home page redirects to articles list"""

    pattern_name = "articles:list"


class ArticleListView(ListView):
    """Display all articles in a table format"""

    model = Article
    template_name = "articles/list.html"
    context_object_name = "articles"
    queryset = Article.objects.select_related("author").order_by("-created")


class CustomLoginView(LoginView):
    """Custom login view with error handling"""

    template_name = "registration/login.html"
    success_url = reverse_lazy("articles:home")

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password. Please try again.")
        return super().form_invalid(form)


class RegisterView(CreateView):
    """User registration view using CreateView only"""

    form_class = UserCreationForm
    template_name = "articles/register.html"
    success_url = reverse_lazy("articles:home")

    def dispatch(self, request, *args, **kwargs):
        # Redirect authenticated users to home page
        if request.user.is_authenticated:
            messages.info(request, "You are already logged in.")
            return redirect("articles:home")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(
            self.request,
            f"Welcome {user.username}! Your account has been created successfully.",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    """Custom logout view with message"""

    next_page = reverse_lazy("articles:home")

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You have been logged out successfully.")
        return super().dispatch(request, *args, **kwargs)


class UserPublicationsView(LoginRequiredMixin, ListView):
    """Display articles published by the current user"""

    model = Article
    template_name = "articles/publications.html"
    context_object_name = "articles"

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user).order_by("-created")


class ArticleDetailView(DetailView):
    """Display detailed view of a single article"""

    model = Article
    template_name = "articles/detail.html"
    context_object_name = "article"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["is_favourite"] = UserFavouriteArticle.objects.filter(
                user=self.request.user, article=context["article"]
            ).exists()
        else:
            context["is_favourite"] = False
        return context


class UserFavouritesView(LoginRequiredMixin, ListView):
    """Display user's favourite articles"""

    model = UserFavouriteArticle
    template_name = "articles/favourites.html"
    context_object_name = "favourites"

    def get_queryset(self):
        return UserFavouriteArticle.objects.filter(
            user=self.request.user
        ).select_related("article")


class PublishView(LoginRequiredMixin, CreateView):
    """Publish a new article using CreateView only"""

    model = Article
    form_class = ArticleForm
    template_name = "articles/publish.html"
    success_url = reverse_lazy("articles:publications")

    def form_valid(self, form):
        # Author field filled automatically during validation
        form.instance.author = self.request.user
        messages.success(
            self.request,
            f"Article '{form.instance.title}' has been published successfully!",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


class AddToFavouriteView(LoginRequiredMixin, CreateView):
    """Add article to favourites using CreateView only"""

    model = UserFavouriteArticle
    fields = []  # No visible fields in the form
    template_name = "articles/add_favourite.html"

    def get_success_url(self):
        return reverse_lazy("articles:detail", kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form):
        # Article field pre-filled with current article ID
        article = get_object_or_404(Article, pk=self.kwargs["pk"])
        form.instance.article = article
        # User field filled with connected user ID during validation
        form.instance.user = self.request.user

        # Check if already in favourites
        if UserFavouriteArticle.objects.filter(
            user=self.request.user, article=article
        ).exists():
            messages.warning(
                self.request, f"'{article.title}' is already in your favourites."
            )
            return redirect(self.get_success_url())

        messages.success(self.request, f"Added '{article.title}' to your favourites!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["article"] = get_object_or_404(Article, pk=self.kwargs["pk"])
        return context


class ToggleFavouriteView(LoginRequiredMixin, View):
    """Toggle favourite status of an article"""

    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        favourite, created = UserFavouriteArticle.objects.get_or_create(
            user=request.user, article=article
        )

        if not created:
            favourite.delete()
            is_favourite = False
            message = f"Removed '{article.title}' from favourites"
        else:
            is_favourite = True
            message = f"Added '{article.title}' to favourites"

        messages.success(request, message)

        # Return JSON response for AJAX requests
        if request.headers.get("Content-Type") == "application/json":
            return JsonResponse({"is_favourite": is_favourite, "message": message})

        # Redirect for regular form submission
        return redirect("articles:detail", pk=pk)


class ArticleDeleteView(LoginRequiredMixin, View):
    """Delete an article (only author can delete)"""

    def get(self, request, pk):
        """Display confirmation page"""
        print(f"GET request received for article {pk}")  # Debug log
        article = get_object_or_404(Article, pk=pk, author=request.user)
        return render(request, "articles/simple_delete.html", {"article": article})

    def post(self, request, pk):
        """Handle the delete request"""
        print(f"POST request received for article {pk}")  # Debug log
        article = get_object_or_404(Article, pk=pk, author=request.user)
        article_title = article.title
        print(f"About to delete article: {article_title}")  # Debug log

        # Delete the article (CASCADE will handle related objects)
        article.delete()
        print(f"Article {article_title} deleted successfully")  # Debug log

        messages.success(
            request, f"Article '{article_title}' has been deleted successfully."
        )
        return redirect("articles:publications")
