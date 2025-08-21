from django.http import HttpResponse
from django.urls import path

from . import views


def home(request):
    return HttpResponse("""
    <html>
    <head><title>Ex06</title></head>
    <body>
        <p>Try accessing:
            <a href="/ex06/init">init</a> |
            <a href="/ex06/populate">populate</a> |
            <a href="/ex06/display">display</a> |
            <a href="/ex06/update">update</a> |
        </p>
    </body>
    </html>
    """)


urlpatterns = [
    path("", home, name="home"),
    path("init", views.init, name="init"),
    path("populate", views.populate, name="populate"),
    path("display", views.display, name="display"),
    path("update", views.update, name="update"),
]
