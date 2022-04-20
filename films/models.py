from django.db import models
from django_countries.fields import CountryField


class Genre(models.Model):
    genre_name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.genre_name


class Language(models.Model):
    lang = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.lang


class Movie(models.Model):
    title = models.CharField(max_length=60)
    production_year = models.IntegerField()
    genres = models.ManyToManyField(Genre)
    duration = models.IntegerField()
    countries = CountryField(multiple=True)
    languages = models.ManyToManyField(Language, blank=True)
    rating = models.FloatField()
    total_votes = models.IntegerField()
    '''
    Director, writer and actor fields as a TextField for now,
    create person model for more details.
    '''
    director = models.TextField(max_length=200)
    writer = models.TextField(max_length=200)
    actors = models.TextField(max_length=500)
    description = models.TextField(max_length=600)

    def __str__(self):
        return self.title


