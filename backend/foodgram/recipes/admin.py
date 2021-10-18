from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (ShoppingCard,
                     Recipe,
                     Ingredients,
                     Components,
                     Tag,
                     Favorite
                     )


class TagAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'name',
                    'color',
                    'slug')


class component_inline(admin.TabularInline):
    model = Components
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (component_inline,)
    list_display = ('name',
                    'author',
                    'text',
                    'cooking_time',
                    'in_favorite')

    readonly_fields = ('in_favorite',)
    list_filter = ('name', 'author', 'tag')

    def in_favorite(self, obj):
        count = Favorite.objects.filter(recipe=obj).count()
        return count


class IngredientsAdmin(admin.ModelAdmin):

    list_display = ('name',
                    'measurement_unit')
    list_filter = ('name',)


class ComponentsAdmin(admin.ModelAdmin):

    list_display = ( 'ingredient', 'component_in_recipe', 'amount')

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', )

class ShoppingCardAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', )

admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(Components, ComponentsAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCard, ShoppingCardAdmin)