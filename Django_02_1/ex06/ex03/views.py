# Create your views here.
import psycopg2
from django.conf import settings
from django.http import HttpResponse


def populate(request):
    movies_data = [
        (1, "The Phantom Menace", "George Lucas", "Rick McCallum", "1999-05-19"),
        (2, "Attack of the Clones", "George Lucas", "Rick McCallum", "2002-05-16"),
        (3, "Revenge of the Sith", "George Lucas", "Rick McCallum", "2005-05-19"),
        (4, "A New Hope", "George Lucas", "Gary Kurtz, Rick McCallum", "1977-05-25"),
        (
            5,
            "The Empire Strikes Back",
            "Irvin Kershner",
            "Gary Kurtz, Rick McCallum",
            "1980-05-17",
        ),
        (
            6,
            "Return of the Jedi",
            "Richard Marquand",
            "Howard G. Kazanjian, George Lucas, Rick McCallum",
            "1983-05-25",
        ),
        (
            7,
            "The Force Awakens",
            "J. J. Abrams",
            "Kathleen Kennedy, J. J. Abrams, Bryan Burk",
            "2015-12-11",
        ),
    ]
    results = []
    try:
        conn = psycopg2.connect(
            dbname=settings.DATABASES["default"]["NAME"],
            user=settings.DATABASES["default"]["USER"],
            password=settings.DATABASES["default"]["PASSWORD"],
            host=settings.DATABASES["default"]["HOST"],
            port=settings.DATABASES["default"]["PORT"],
        )
        cursor = conn.cursor()
        for m in movies_data:
            try:
                cursor.execute(
                    """
                    INSERT INTO ex03_movies (episode_nb, title, director, producer, release_date)
                    VALUES (%s, %s, %s, %s, %s)
                """,
                    m,
                )
                conn.commit()
                results.append("OK")
            except Exception as e:
                results.append(f"Erreur pour {m[1]} : {str(e)}")
        cursor.close()
        conn.close()
        return HttpResponse("<br>".join(results))
    except Exception as e:
        return HttpResponse(f"Erreur : {str(e)}")


def display(request):
    try:
        conn = psycopg2.connect(
            dbname=settings.DATABASES["default"]["NAME"],
            user=settings.DATABASES["default"]["USER"],
            password=settings.DATABASES["default"]["PASSWORD"],
            host=settings.DATABASES["default"]["HOST"],
            port=settings.DATABASES["default"]["PORT"],
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ex03_movies ORDER BY episode_nb;")
        movies = cursor.fetchall()
        cursor.close()
        conn.close()
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
                <td>{m[0]}</td>
                <td>{m[1]}</td>
                <td>{m[2] if m[2] else ""}</td>
                <td>{m[3]}</td>
                <td>{m[4]}</td>
                <td>{m[5]}</td>
            </tr>
            """
        html += "</table>"
        return HttpResponse(html)
    except Exception:
        return HttpResponse("No data available")
