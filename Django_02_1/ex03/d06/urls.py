"""
URL configuration for d06 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path


def home(request):
    return HttpResponse("""
    <html>
    <head><title>Welcome to Django</title></head>
    <body>
        <h1>The install worked successfully! Congratulations!</h1>
        <p>Try accessing:
            <a href="/ex00/init">ex00</a> |
            <a href="/ex01/test-str">ex01</a> |
            <a href="/ex02">ex02</a> |
            <a href="/ex03">ex03</a> |
        </p>
    </body>
    </html>
    """)


urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("ex00/", include("ex00.urls")),
    path("ex01/", include("ex01.urls")),
    path("ex02/", include("ex02.urls")),
    path("ex03/", include("ex03.urls")),
]
