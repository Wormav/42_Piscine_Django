from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, RedirectView

from .models import Article


class HomeView(RedirectView):
    """Home page redirects to articles list"""

    pattern_name = "articles:list"


class ArticleListView(ListView):
    """Display all articles in a table format"""

    model = Article
    template_name = "articles/list.html"
    context_object_name = "articles"
    queryset = Article.objects.select_related("author").all()


class CustomLoginView(LoginView):
    """Custom login view with error handling"""

    template_name = "registration/login.html"
    success_url = reverse_lazy("articles:home")

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password. Please try again.")
        return super().form_invalid(form)


class SignUpView(CreateView):
    """User registration view"""

    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("articles:home")

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
