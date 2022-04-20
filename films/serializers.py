from rest_framework import serializers
from django_countries.serializer_fields import CountryField
from django_countries.serializers import CountryFieldMixin

from .models import Movie, Language, Genre


class GenreSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return value.genre_name


class LanguageSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return value.lang


class DynamicFieldsSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class MovieSerializer(CountryFieldMixin, DynamicFieldsSerializer):
    languages = LanguageSerializer(read_only=True, many=True)
    genres = GenreSerializer(read_only=True, many=True)

    class Meta:
        model = Movie
        fields = '__all__'


