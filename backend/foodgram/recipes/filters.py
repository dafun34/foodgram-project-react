import django_filters as filters

from .models import Recipe


class TagFilter(filters.FilterSet):

    tag = filters.AllValuesMultipleFilter(field_name='tags__slug')
    author = filters.CharFilter(field_name='author__username')

    class Meta:
        model = Recipe
        fields = ('tags', 'author')
