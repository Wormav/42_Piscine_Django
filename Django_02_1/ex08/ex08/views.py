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
        base_dir = settings.BASE_DIR
        planets_path = os.path.join(base_dir, "ex08", "planets.csv")
        people_path = os.path.join(base_dir, "ex08", "people.csv")

        if not os.path.exists(planets_path):
            with open(planets_path, "w") as f:
                f.write(
                    "name,climate,diameter,orbital_period,population,rotation_period,surface_water,terrain\n"
                )
        if not os.path.exists(people_path):
            with open(people_path, "w") as f:
                f.write(
                    "name,birth_year,gender,eye_color,hair_color,height,mass,homeworld\n"
                )

        return HttpResponse("OK")
    except Exception as e:
        return HttpResponse(f"Erreur : {str(e)}")


def populate(request):
    results = []
    base_dir = settings.BASE_DIR
    planets_csv = os.path.join(base_dir, "ex08", "planets.csv")
    people_csv = os.path.join(base_dir, "ex08", "people.csv")

    fake_planets = [
        "Bespin,windy,118000,5110,6000000,12,8,gas giant\n",
        "Kamino,moderately windy,19720,463,1000000000,27,100,ocean\n",
        "Tatooine,arid,10465,304,200000,23,1,desert\n",
    ]
    with open(planets_csv, "w") as f:
        f.write(
            "name,climate,diameter,orbital_period,population,rotation_period,surface_water,terrain\n"
        )
        f.writelines(fake_planets)

    fake_people = [
        "Lobot,37BBY,male,blue,none,175,79,Bespin\n",
        "Taun We,unknown,female,black,none,213,0,Kamino\n",
        "Luke Skywalker,19BBY,male,blue,blond,172,77,Tatooine\n",
    ]
    with open(people_csv, "w") as f:
        f.write("name,birth_year,gender,eye_color,hair_color,height,mass,homeworld\n")
        f.writelines(fake_people)

    try:
        conn = psycopg2.connect(
            dbname=settings.DATABASES["default"]["NAME"],
            user=settings.DATABASES["default"]["USER"],
            password=settings.DATABASES["default"]["PASSWORD"],
            host=settings.DATABASES["default"]["HOST"],
            port=settings.DATABASES["default"]["PORT"],
        )
        cursor = conn.cursor()

        # Vider les tables avant insertion
        cursor.execute("TRUNCATE TABLE ex08_people CASCADE;")
        cursor.execute("TRUNCATE TABLE ex08_planets CASCADE;")
        conn.commit()

        try:
            with open(planets_csv, "r") as f:
                next(f)  # skip header
                cursor.copy_from(
                    f,
                    "ex08_planets",
                    sep=",",
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
        except Exception as e:
            results.append(f"Erreur planets : {str(e)}")

        try:
            with open(people_csv, "r") as f:
                next(f)  # skip header
                cursor.copy_from(
                    f,
                    "ex08_people",
                    sep=",",
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
        except Exception as e:
            results.append(f"Erreur people : {str(e)}")
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
        cursor.execute("""
            SELECT p.name, p.homeworld, pl.climate
            FROM ex08_people p
            JOIN ex08_planets pl ON p.homeworld = pl.name
            WHERE pl.climate IN ('windy', 'moderately windy')
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
