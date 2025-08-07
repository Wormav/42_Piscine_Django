from django.urls import path
from . import views

urlpatterns = [
	path('django', views.django, name='ex01_django'),
 	path('display', views.display, name='ex01_display'),
    path('templates', views.templates, name='ex01_templates'),
]
