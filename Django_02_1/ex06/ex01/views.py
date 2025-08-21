from datetime import date

from django.http import HttpResponse

from .models import Movies


def test_str(request):
    # Create one movie
    movie = Movies(
        episode_nb=999,
        title="Test Movie",
        director="Test Director",
        producer="Test Producer",
        release_date=date.today(),
    )
    movie.save()

    # Testing __str__
    result = str(movie)

    # delete
    movie.delete()

    return HttpResponse(f"La méthode __str__ return: '{result}'")
