from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (User,
                     Recipe,
                     Ingredients,
                     Tag,
                     Components,
                     Favorite,
                     Follow,
                     Cart)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'cooking_time')


class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')


class ComponentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredients', 'amount')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(Components, ComponentsAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Cart, CartAdmin)