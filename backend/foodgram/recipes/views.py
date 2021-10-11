from django.shortcuts import render
from rest_framework import viewsets
from .models import Recipe, Components, Ingredients, Tag
from .serializers import (RecipeListSerializer,
                          ComponentsListSerializer,
                          IngredientsSerializer,
                          RecipeCreateSerializer,
                          ComponentsCreateSerializer,
                          TagsSerializer,
                          )




class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return RecipeCreateSerializer
        return RecipeListSerializer


class ComponentsViewSet(viewsets.ModelViewSet):
    queryset = Components.objects.all()

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return ComponentsCreateSerializer
        return ComponentsListSerializer
