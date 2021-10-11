from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (User,
                     Recipe,
                     Ingredients,
                     Components,
                     Tag
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
    list_display = ('name', 'cooking_time')


class IngredientsAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'measurement_unit')


class ComponentsAdmin(admin.ModelAdmin):

    list_display = ( 'ingredient', 'component_in_recipe', 'amount')

admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(Components, ComponentsAdmin)
