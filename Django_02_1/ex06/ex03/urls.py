from django.http import HttpResponse
from django.urls import path

from . import views


def home(request):
    return HttpResponse("""
    <html>
    <head><title>Ex03</title></head>
    <body>
        <p>Try accessing:
            <a href="/ex03/populate">populate</a> |
            <a href="/ex03/display">display</a> |
        </p>
    </body>
    </html>
    """)


urlpatterns = [
    path("", home, name="home"),
    path("populate", views.populate, name="populate"),
    path("display", views.display, name="display"),
]
