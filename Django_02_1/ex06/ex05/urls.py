from django.http import HttpResponse
from django.urls import path

from . import views


def home(request):
    return HttpResponse("""
    <html>
    <head><title>Ex05</title></head>
    <body>
        <p>Try accessing:
            <a href="/ex05/populate">populate</a> |
            <a href="/ex05/display">display</a> |
            <a href="/ex05/remove">remove</a> |
        </p>
    </body>
    </html>
    """)


urlpatterns = [
    path("", home, name="home"),
    path("populate", views.populate, name="populate"),
    path("display", views.display, name="display"),
    path("remove", views.remove, name="remove"),
]
