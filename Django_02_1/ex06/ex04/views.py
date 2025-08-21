# Create your views here.
import psycopg2
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


def init(request):
    try:
        conn = psycopg2.connect(
            dbname=settings.DATABASES["default"]["NAME"],
            user=settings.DATABASES["default"]["USER"],
            password=settings.DATABASES["default"]["PASSWORD"],
            host=settings.DATABASES["default"]["HOST"],
            port=settings.DATABASES["default"]["PORT"],
        )
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ex04_movies (
                episode_nb INTEGER PRIMARY KEY,
                title VARCHAR(64) UNIQUE NOT NULL,
                opening_crawl TEXT,
                director VARCHAR(32) NOT NULL,
                producer VARCHAR(128) NOT NULL,
                release_date DATE NOT NULL
            );
        """)
        conn.commit()
        cursor.close()
        conn.close()
        return HttpResponse("OK")
    except Exception as e:
        return HttpResponse(f"Erreur : {str(e)}")


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
                    "SELECT 1 FROM ex04_movies WHERE episode_nb = %s;", (m[0],)
                )
                if cursor.fetchone():
                    results.append(f"{m[1]} already present")
                    continue
                cursor.execute(
                    """
                    INSERT INTO ex04_movies (episode_nb, title, director, producer, release_date)
                    VALUES (%s, %s, %s, %s, %s)
                """,
                    m,
                )
                conn.commit()
                results.append("OK")
            except Exception as e:
                results.append(f"Error for {m[1]} : {str(e)}")
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
        cursor.execute("SELECT * FROM ex04_movies ORDER BY episode_nb;")
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


@csrf_exempt
def remove(request):
    try:
        conn = psycopg2.connect(
            dbname=settings.DATABASES["default"]["NAME"],
            user=settings.DATABASES["default"]["USER"],
            password=settings.DATABASES["default"]["PASSWORD"],
            host=settings.DATABASES["default"]["HOST"],
            port=settings.DATABASES["default"]["PORT"],
        )
        cursor = conn.cursor()
        if request.method == "POST":
            title = request.POST.get("title")
            cursor.execute("DELETE FROM ex04_movies WHERE title = %s;", (title,))
            conn.commit()
        cursor.execute("SELECT title FROM ex04_movies ORDER BY episode_nb;")
        titles = cursor.fetchall()
        cursor.close()
        conn.close()
        if not titles:
            return HttpResponse("No data available")
        html = """
        <form method="post">
            <select name="title">
        """
        for t in titles:
            html += f'<option value="{t[0]}">{t[0]}</option>'
        html += """
            </select>
            <button type="submit" name="remove">remove</button>
        </form>
        """
        return HttpResponse(html)
    except Exception:
        return HttpResponse("No data available")
