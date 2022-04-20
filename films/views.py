from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator

from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from .models import Movie, Genre, Language
from .forms import SearchForm, SearchAdvancedAPI
from .serializers import MovieSerializer


DURATION_SELECT = {
    'S': (60, 1),
    'N': (120, 60),
    'L': (999, 120)
}


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 50


class MovieViewAPI(generics.ListAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = MovieSerializer

    def get_queryset(self):
        if 'search_advanced_api' in self.request.session:
            data = self.request.session['search_advanced_api']
            if data['duration_choice']:
                duration1, duration2 = DURATION_SELECT[data['duration_choice']]
            else:
                duration1 = 999
                duration2 = 1

            movies = Movie.objects.filter(
                production_year__range=(data['year_min'], data['year_max']),
                duration__range=(duration2, duration1),
                rating__range=(data['rating_min'], data['rating_max'])
            ).distinct()
            if data['genres']:
                movies = movies.filter(genres__in=[Genre.objects.get(genre_name=data['genres'][0])])
            return movies
        else:
            return Movie.objects.all()

    def list(self, request):
        fields = None
        if 'search_advanced_api' in self.request.session:
            fields = self.request.session['search_advanced_api']['parameters']
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = MovieSerializer(page, many=True, fields=fields)
        return self.get_paginated_response(serializer.data)


class AllMoviesView(ListView):
    genres = Genre.objects.all()

    def get(self, *args, **kwargs):
        try:
            genre = Genre.objects.get(genre_name=self.request.GET.get('genre', -1))
            if 'advanced_search' in self.request.session:
                del self.request.session['advanced_search']
            if genre in Genre.objects.all():
                self.request.session['genre'] = genre.genre_name
                movies = Movie.objects.filter(genres__in=[Genre.objects.get(genre_name=self.request.session['genre'])])
            else:
                movies = Movie.objects.all()
        except ObjectDoesNotExist:
            if 'advanced_search' in self.request.session:
                if self.request.session['advanced_search']['duration_choice']:
                    duration1, duration2 = DURATION_SELECT[self.request.session['advanced_search']['duration_choice']]
                else:
                    duration1 = 999
                    duration2 = 1
                movies = Movie.objects.filter(
                    production_year__range=(self.request.session['advanced_search']['year_min'],
                                            self.request.session['advanced_search']['year_max']),
                    duration__range=(duration2, duration1),
                    rating__range=(self.request.session['advanced_search']['rating_min'],
                                   self.request.session['advanced_search']['rating_max'])
                )
                if 'genres' in self.request.session['advanced_search']:
                    for gen in self.request.session['advanced_search']['genres']:
                        movies = movies.filter(
                            genres__in=[Genre.objects.get(genre_name=gen)]
                        )
            elif 'genre' in self.request.session:
                movies = Movie.objects.filter(genres__in=[Genre.objects.get(genre_name=self.request.session['genre'])])
            else:
                movies = Movie.objects.all()
        paginator = Paginator(movies, 20)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        search_form = SearchForm()
        context = {
            'all_movies': movies,
            'all_genres': self.genres,
            'search_form': search_form,
            'page_obj': page_obj
        }
        return render(self.request, 'movies_list.html', context)

    def post(self, *args, **kwargs):
        form = SearchForm(self.request.POST)
        if form.is_valid():
            self.request.session['advanced_search'] = form.cleaned_data
            data = form.cleaned_data
            if data['duration_choice']:
                duration1, duration2 = DURATION_SELECT[data['duration_choice']]
            else:
                duration1 = 999
                duration2 = 1

            movies = Movie.objects.filter(
                production_year__range=(data['year_min'], data['year_max']),
                duration__range=(duration2, duration1),
                rating__range=(data['rating_min'], data['rating_max'])
            ).distinct()
            if data['genres']:
                for gen in data['genres']:
                    movies = movies.filter(
                        genres__in=[Genre.objects.get(genre_name=gen)]
                    )

            paginator = Paginator(movies, 20)
            page_number = 1
            page_obj = paginator.get_page(page_number)

            context = {
                'all_movies': movies,
                'all_genres': self.genres,
                'search_form': form,
                'page_obj': page_obj
            }
            return render(self.request, 'movies_list.html', context)

        else:
            return redirect('films:all-movies')


class DetailedMovieView(DetailView):
    def get(self, request, pk, *args, **kwargs):
        movie = Movie.objects.get(pk=pk)
        genres = movie.genres.all()
        related = Movie.objects.filter(genres__in=genres).order_by('?')[:4]
        context = {
            'movie': movie,
            'related': related
        }
        return render(self.request, 'movie_details.html', context)


class AdvancedSearchView(View):
    def get(self, *args, **kwargs):
        form = SearchAdvancedAPI()
        context = {
            'search_form': form
        }
        return render(self.request, 'advanced_search.html', context)

    def post(self, *args, **kwargs):
        form = SearchAdvancedAPI(self.request.POST or None)
        if form.is_valid():
            self.request.session['search_advanced_api'] = form.cleaned_data
        return redirect('films:movies-get')


def home_view(request):
    if 'advanced_search' in request.session:
        del request.session['advanced_search']
    if 'genre' in request.session:
        del request.session['genre']
    if 'search_advanced_api' in request.session:
        del request.session['search_advanced_api']
    return redirect('films:all-movies')



