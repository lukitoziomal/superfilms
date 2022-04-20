from django.urls import path, include
from rest_framework import routers
from . import views


router = routers.DefaultRouter()

app_name = 'films'
urlpatterns = [
    path('', views.AllMoviesView.as_view(), name='all-movies'),
    path('', include(router.urls)),
    path('movies-get', views.MovieViewAPI.as_view(), name='movies-get'),
    path('details/<int:pk>', views.DetailedMovieView.as_view(), name='detailed-view'),
    path('api-search', views.AdvancedSearchView.as_view(), name='advanced-search'),
    path('home', views.home_view, name='delete-session'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]