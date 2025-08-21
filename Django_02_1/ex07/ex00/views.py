# Create your views here.
import psycopg2
from django.conf import settings
from django.http import HttpResponse


def init(request):
    try:
        # Connexion db
        conn = psycopg2.connect(
            dbname=settings.DATABASES["default"]["NAME"],
            user=settings.DATABASES["default"]["USER"],
            password=settings.DATABASES["default"]["PASSWORD"],
            host=settings.DATABASES["default"]["HOST"],
            port=settings.DATABASES["default"]["PORT"],
        )

        cursor = conn.cursor()

        # Create table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS ex00_movies (
            episode_nb INTEGER PRIMARY KEY,
            title VARCHAR(64) UNIQUE NOT NULL,
            opening_crawl TEXT,
            director VARCHAR(32) NOT NULL,
            producer VARCHAR(128) NOT NULL,
            release_date DATE NOT NULL
        );
        """
        cursor.execute(create_table_query)
        conn.commit()

        cursor.close()
        conn.close()

        return HttpResponse("OK")

    except Exception as e:
        return HttpResponse(f"Erreur : {str(e)}")
