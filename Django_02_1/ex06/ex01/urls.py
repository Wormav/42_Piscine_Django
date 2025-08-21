from django.urls import path

from . import views

urlpatterns = [
    path("test-str/", views.test_str, name="test_str"),
]
