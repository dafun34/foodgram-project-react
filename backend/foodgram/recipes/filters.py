import django_filters as filters

from .models import Recipe, Tag


class TagFilter(filters.FilterSet):

    tag = filters.AllValuesMultipleFilter(field_name='tag__slug')
    author = filters.CharFilter(field_name='author__username')
    class Meta:
        model = Recipe
        fields = ('tag', 'author')