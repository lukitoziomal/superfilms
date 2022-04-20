import csv
from django_countries import countries
from films.models import Movie, Language, Genre


def run():
    """use movies10.csv for DB sample of few movies
        or movies.csv for over 25k results, it will take a while to load"""
    # mfile = open('movies10.csv', encoding='utf-8')
    mfile = open('movies.csv', encoding='utf-8')
    reader = csv.reader(mfile, delimiter=';')

    Movie.objects.all().delete()
    Genre.objects.all().delete()
    Language.objects.all().delete()

    """
    2 - title
    3 - production_year
    4 - genres
    5 - duration
    6 - countries
    7 - languages
    8 - director
    9 - writer
    10 - actors
    11 - description
    12 - rating
    13 - total_votes
    """

    for row in reader:
        print('>>', row[2])
        try:
            movie = Movie.objects.create(
                title=row[2],
                production_year=row[3],
                duration=row[5],
                rating=row[12],
                total_votes=row[13],
                director=row[8],
                writer=row[9],
                actors=row[10],
                description=row[11]
            )
            for genre in row[4].split(', '):
                gen, created = Genre.objects.get_or_create(
                    genre_name=genre
                )
                gen.save()
                movie.genres.add(gen)

            for language in row[7].split(', '):
                if language != '' and language != 'None':
                    langg, created = Language.objects.get_or_create(
                        lang=language.lower()
                    )
                    langg.save()
                    movie.languages.add(langg)

            digit_countries = ''
            for country in row[6].split(', '):
                for key, val in dict(countries).items():
                    if val == country or (country == 'USA' and key == 'US'):
                        digit_countries += key + ','
            movie.countries = digit_countries
            movie.save()
        except Exception:
            print('wrong date type, skipping')
