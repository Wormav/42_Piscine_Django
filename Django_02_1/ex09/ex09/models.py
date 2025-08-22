from django.db import models


class Planets(models.Model):
    name = models.CharField(max_length=64, unique=True, null=False)
    climate = models.CharField(max_length=255, blank=True)
    diameter = models.IntegerField(blank=True, null=True)
    orbital_period = models.IntegerField(blank=True, null=True)
    population = models.BigIntegerField(blank=True, null=True)
    rotation_period = models.IntegerField(blank=True, null=True)
    surface_water = models.FloatField(blank=True, null=True)
    terrain = models.CharField(max_length=255, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "ex09_planets"


class People(models.Model):
    name = models.CharField(max_length=64, null=False)
    birth_year = models.CharField(max_length=32)
    gender = models.CharField(max_length=32)
    eye_color = models.CharField(max_length=32)
    hair_color = models.CharField(max_length=32)
    height = models.IntegerField()
    mass = models.FloatField()
    homeworld = models.ForeignKey(
        Planets, on_delete=models.CASCADE, null=True, blank=True
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
