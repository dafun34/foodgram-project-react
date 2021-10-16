from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import SAFE_METHODS, AllowAny
from rest_framework.response import Response
from .models import Recipe, Components, Ingredients, Tag, Favorite, ShoppingCard
from .serializers import (RecipeListSerializer,
                          ComponentsListSerializer,
                          IngredientsSerializer,
                          RecipeCreateSerializer,
                          ComponentsCreateSerializer,
                          TagsSerializer,
                          FavoriteCreateSerializer,
                          FavoriteRecipeViewSerializer,
                          ShoppingCardAddRecipeSerializer
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
        recipe = get_object_or_404(Recipe, id=recipe_id)
        user = self.request.user.id
        data = {'user': user, 'recipe': recipe.id}
        context = {'request': request}
        serializer = FavoriteCreateSerializer(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        recipe_serializer = FavoriteRecipeViewSerializer(recipe)
        return Response(recipe_serializer.data, status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        user = self.request.user
        favorite = get_object_or_404(Favorite, user=user, recipe=recipe)
        favorite.delete()
        return Response(status.HTTP_204_NO_CONTENT)


class CardAddRecipeView(APIView):
    def get(self, request, recipe_id):
        user = self.request.user.id
        recipe = get_object_or_404(Recipe, id=recipe_id)
        data = {'user': user, 'recipe':recipe.id}
        context = {'request': request}
        serializer = ShoppingCardAddRecipeSerializer(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        detail = {'detail':'рецепт успешно добавлен в корзину'}
        recipe_serializer = FavoriteRecipeViewSerializer(recipe)
        return Response(recipe_serializer.data, status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        user = self.request.user
        object = ShoppingCard.objects.get(user=user, recipe=recipe)
        object.delete()
        return Response(status.HTTP_204_NO_CONTENT)

