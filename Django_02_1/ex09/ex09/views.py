from django.http import HttpResponse
from django.shortcuts import render

from .models import People


def display(request):
    try:
        # Filtrer les personnages dont la planète d'origine a un climat "windy" ou "moderately windy"
        # et trier par ordre alphabétique du nom du personnage
        people = (
            People.objects.filter(homeworld__climate__icontains="windy")
            .order_by("name")
            .select_related("homeworld")
        )

        if not people:
            # Si aucune donnée n'est disponible
            message = """No data available, please use the following command line before use:

python manage.py loaddata ex09_initial_data.json"""
            return HttpResponse(message, content_type="text/plain")

        context = {"people": people}
        return render(request, "ex09/display.html", context)

    except Exception:
        message = """No data available, please use the following command line before use:

python manage.py loaddata ex09_initial_data.json"""
        return HttpResponse(message, content_type="text/plain")
