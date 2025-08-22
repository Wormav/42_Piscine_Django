from django.http import HttpResponse
from django.urls import path

from . import views


def home(request):
    return HttpResponse("""
    <html>
    <head><title>Ex09</title></head>
    <body>
        <p>Try accessing:
            <a href="/ex09/display">display</a>
        </p>
    </body>
    </html>
    """)


urlpatterns = [
    path("", home, name="home"),
    path("display/", views.display, name="display"),
]
