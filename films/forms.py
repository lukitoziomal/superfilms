from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Genre, Language, Movie


DURATION_CHOICES = (
    ('S', '< 60 minutes'),
    ('N', '60 - 120 minutes'),
    ('L', '> 120 minutes')
)


class SearchForm(forms.Form):
    genres = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=[(genre.genre_name, genre.genre_name) for genre in Genre.objects.all()],
    )
    year_min = forms.IntegerField(
        min_value=1900,
        max_value=2021,
        required=False,
    )
    year_max = forms.IntegerField(
        min_value=1901,
        max_value=2022,
        required=False
    )
    duration_choice = forms.ChoiceField(
        required=False,
        choices=DURATION_CHOICES
    )
    rating_min = forms.FloatField(
        min_value=1,
        max_value=10,
        required=False
    )
    rating_max = forms.FloatField(
        min_value=1.1,
        max_value=10,
        required=False
    )

    def clean(self):
        cleaned_data = super().clean()
        year_min = cleaned_data['year_min']
        year_max = cleaned_data['year_max']
        rating_min = cleaned_data['rating_min']
        rating_max = cleaned_data['rating_max']
        if year_min > year_max:
            raise forms.ValidationError(_('year_min > year_max'))
        if rating_min > rating_max:
            raise forms.ValidationError(_('rating_min > rating_max'))


class SearchAdvancedAPI(SearchForm):
    parameters = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        choices=[(field.name, field.name) for field in Movie._meta.get_fields()]
    )