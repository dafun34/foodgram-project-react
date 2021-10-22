from django.contrib import admin

from .models import (Components, Favorite, Ingredients, Recipe, ShoppingCard,
                     Tag)


class TagAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'name',
                    'color',
                    'slug')


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'author',
                    'text',
                    'cooking_time',
                    'in_favorite')

    readonly_fields = ('in_favorite',)
    list_filter = ('name', 'author', 'tags')

    def in_favorite(self, obj):
        return Favorite.objects.filter(recipe=obj).count()


class IngredientsAdmin(admin.ModelAdmin):

    list_display = ('name',
                    'measurement_unit')
    list_filter = ('name',)


class ComponentsAdmin(admin.ModelAdmin):

    list_display = ('name', 'component_in_recipe', 'amount')


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', )


class ShoppingCardAdmin(admin.ModelAdmin):
    list_display = ('user', )


admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(Components, ComponentsAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCard, ShoppingCardAdmin)
