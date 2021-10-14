from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import SAFE_METHODS, AllowAny
from rest_framework.response import Response
from .models import Recipe, Components, Ingredients, Tag, Favorite
from .serializers import (RecipeListSerializer,
                          ComponentsListSerializer,
                          IngredientsSerializer,
                          RecipeCreateSerializer,
                          ComponentsCreateSerializer,
                          TagsSerializer,
                          FavoriteCreateSerializer
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

class FavoriteCreate(APIView):
    def get(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, recipe_id)
        user = self.request.user.id
        data = {'user': user, 'recipe': recipe.id}
        serializer = FavoriteCreateSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
