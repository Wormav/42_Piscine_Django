from datetime import date

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Movies


def populate(request):
    movies_data = [
        (1, "The Phantom Menace", "George Lucas", "Rick McCallum", date(1999, 5, 19)),
        (2, "Attack of the Clones", "George Lucas", "Rick McCallum", date(2002, 5, 16)),
        (3, "Revenge of the Sith", "George Lucas", "Rick McCallum", date(2005, 5, 19)),
        (
            4,
            "A New Hope",
            "George Lucas",
            "Gary Kurtz, Rick McCallum",
            date(1977, 5, 25),
        ),
        (
            5,
            "The Empire Strikes Back",
            "Irvin Kershner",
            "Gary Kurtz, Rick McCallum",
            date(1980, 5, 17),
        ),
        (
            6,
            "Return of the Jedi",
            "Richard Marquand",
            "Howard G. Kazanjian, George Lucas, Rick McCallum",
            date(1983, 5, 25),
        ),
        (
            7,
            "The Force Awakens",
            "J. J. Abrams",
            "Kathleen Kennedy, J. J. Abrams, Bryan Burk",
            date(2015, 12, 11),
        ),
    ]
    results = []
    for m in movies_data:
        try:
            if not Movies.objects.filter(episode_nb=m[0]).exists():
                Movies.objects.create(
                    episode_nb=m[0],
                    title=m[1],
                    director=m[2],
                    producer=m[3],
                    release_date=m[4],
                )
                results.append("OK")
            else:
                results.append(f"{m[1]} already present")
        except Exception as e:
            results.append(f"Erreur pour {m[1]} : {str(e)}")
    return HttpResponse("<br>".join(results))


def display(request):
    try:
        movies = Movies.objects.all().order_by("episode_nb")
        if not movies:
            return HttpResponse("No data available")
        html = """
        <table border="1">
            <tr>
                <th>Episode</th>
                <th>Title</th>
                <th>Opening Crawl</th>
                <th>Director</th>
                <th>Producer</th>
                <th>Release Date</th>
            </tr>
        """
        for m in movies:
            html += f"""
            <tr>
                <td>{m.episode_nb}</td>
                <td>{m.title}</td>
                <td>{m.opening_crawl if m.opening_crawl else ""}</td>
                <td>{m.director}</td>
                <td>{m.producer}</td>
                <td>{m.release_date}</td>
            </tr>
            """
        html += "</table>"
        return HttpResponse(html)
    except Exception:
        return HttpResponse("No data available")


@csrf_exempt
def remove(request):
    try:
        if request.method == "POST":
            title = request.POST.get("title")
            Movies.objects.filter(title=title).delete()
        movies = Movies.objects.all().order_by("episode_nb")
        if not movies:
            return HttpResponse("No data available")
        html = """
        <form method="post">
            <select name="title">
        """
        for m in movies:
            html += f'<option value="{m.title}">{m.title}</option>'
        html += """
            </select>
            <button type="submit" name="remove">remove</button>
        </form>
        """
        return HttpResponse(html)
    except Exception:
        return HttpResponse("No data available")
