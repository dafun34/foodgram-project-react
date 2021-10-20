import django_filters as filters

from .models import Recipe


class TagFilter(filters.FilterSet):
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = filters.BooleanFilter(method='get_favorited')
    is_in_shopping_cart = filters.BooleanFilter(method='get_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart',)

    def get_favorited(self, queryset, name, value):
        if value:
            return Recipe.objects.filter(favorite__user=self.request.user)
        return Recipe.objects.all()

    def get_shopping_cart(self, queryset, name, value):
        if value:
            return Recipe.objects.filter(
                card_recipe__user=self.request.user
            )
        return Recipe.objects.all()
