"""Файл с фильтрами для приложения app."""

from django_filters import CharFilter, FilterSet
from reviews.models import Title


class TitleFilter(FilterSet):
    """Класс фильтров для вьюсета модели Title."""
    name = CharFilter(field_name='name', lookup_expr='contains')
    category = CharFilter(field_name='category__slug', lookup_expr='exact')
    genre = CharFilter(field_name='genre__slug', lookup_expr='exact')

    class Meta:
        model = Title
        fields = ('name', 'category', 'genre', 'year',)
