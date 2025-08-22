import os

import psycopg2
from django.conf import settings
from django.http import HttpResponse


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
            CREATE TABLE IF NOT EXISTS ex08_planets (
                id SERIAL PRIMARY KEY,
                name VARCHAR(64) UNIQUE NOT NULL,
                climate VARCHAR,
                diameter INTEGER,
                orbital_period INTEGER,
                population BIGINT,
                rotation_period INTEGER,
                surface_water REAL,
                terrain VARCHAR(128)
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ex08_people (
                id SERIAL PRIMARY KEY,
                name VARCHAR(64) UNIQUE NOT NULL,
                birth_year VARCHAR(32),
                gender VARCHAR(32),
                eye_color VARCHAR(32),
                hair_color VARCHAR(32),
                height INTEGER,
                mass REAL,
                homeworld VARCHAR(64) REFERENCES ex08_planets(name)
            );
        """)
        conn.commit()
        cursor.close()
        conn.close()
        return HttpResponse("OK")
    except Exception as e:
        return HttpResponse(f"Erreur : {str(e)}")


def clean_csv(filepath):
    temp_path = filepath + ".tmp"
    with open(filepath, "r") as fin, open(temp_path, "w") as fout:
        for line in fin:
            fout.write(line.replace("NULL", "\\N").replace("\t\t", "\t\\N\t"))
    return temp_path


def populate(request):
    results = []
    base_dir = settings.BASE_DIR
    planets_csv = os.path.join(base_dir, "ex08", "planets.csv")
    people_csv = os.path.join(base_dir, "ex08", "people.csv")

    planets_clean = None
    people_clean = None

    try:
        conn = psycopg2.connect(
            dbname=settings.DATABASES["default"]["NAME"],
            user=settings.DATABASES["default"]["USER"],
            password=settings.DATABASES["default"]["PASSWORD"],
            host=settings.DATABASES["default"]["HOST"],
            port=settings.DATABASES["default"]["PORT"],
        )
        cursor = conn.cursor()

        cursor.execute("TRUNCATE TABLE ex08_people CASCADE;")
        cursor.execute("TRUNCATE TABLE ex08_planets CASCADE;")
        conn.commit()

        planets_clean = clean_csv(planets_csv)
        people_clean = clean_csv(people_csv)

        with open(planets_clean, "r") as f:
            lines = f.readlines()
            print("Contenu du fichier planets_clean :")
            for i, line in enumerate(lines[:5]):
                print(f"Ligne {i}: {repr(line)}")

        with open(planets_clean, "r") as f:
            cursor.copy_from(
                f,
                "ex08_planets",
                sep="\t",
                columns=(
                    "name",
                    "climate",
                    "diameter",
                    "orbital_period",
                    "population",
                    "rotation_period",
                    "surface_water",
                    "terrain",
                ),
            )
        conn.commit()
        results.append("OK planets")

        cursor.execute("SELECT name FROM ex08_planets;")
        planet_names = cursor.fetchall()
        print("Planets insérées :", planet_names)

        with open(people_clean, "r") as f:
            cursor.copy_from(
                f,
                "ex08_people",
                sep="\t",
                columns=(
                    "name",
                    "birth_year",
                    "gender",
                    "eye_color",
                    "hair_color",
                    "height",
                    "mass",
                    "homeworld",
                ),
            )
        conn.commit()
        results.append("OK people")
        cursor.close()
        conn.close()
        os.remove(planets_clean)
        os.remove(people_clean)
        return HttpResponse("<br>".join(results))
    except Exception as e:
        try:
            if planets_clean and os.path.exists(planets_clean):
                os.remove(planets_clean)
            if people_clean and os.path.exists(people_clean):
                os.remove(people_clean)
        except Exception:
            pass
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
        cursor.execute("""
            SELECT p.name, p.homeworld, pl.climate
            FROM ex08_people p
            JOIN ex08_planets pl ON p.homeworld = pl.name
            WHERE pl.climate LIKE '%temperate%'
            ORDER BY p.name ASC;
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        if not rows:
            return HttpResponse("No data available")
        html = """
        <table border="1">
            <tr>
                <th>Name</th>
                <th>Homeworld</th>
                <th>Climate</th>
            </tr>
        """
        for r in rows:
            html += f"""
            <tr>
                <td>{r[0]}</td>
                <td>{r[1]}</td>
                <td>{r[2]}</td>
            </tr>
            """
        html += "</table>"
        return HttpResponse(html)
    except Exception:
        return HttpResponse("No data available")
