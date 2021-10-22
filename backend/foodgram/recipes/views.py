from django_filters.rest_framework import DjangoFilterBackend
from .filters import TagFilter
from django.db.models import Sum
from .pagination import RecipePagination
from prettytable import PrettyTable
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated,
                                        IsAdminUser, AllowAny)
from rest_framework.response import Response
from .models import (Recipe,
                     Components,
                     Ingredients,
                     Tag,
                     Favorite,
                     ShoppingCard)
from .permissions import IsAuthorOrAdminOrReadOnly
from .serializers import (ComponentsSerializer,
                          IngredientsSerializer,
                          RecipeSerializer,
                          ComponentsCreateSerializer,
                          FavoriteRecipeViewSerializer,
                          TagListCreateDelSerializer,
                          # RecipeListSerializer
                          )


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagListCreateDelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    pagination_class = None


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthorOrAdminOrReadOnly, ]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TagFilter


class ComponentsViewSet(viewsets.ModelViewSet):
    queryset = Components.objects.all()

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return ComponentsCreateSerializer
        return ComponentsSerializer


class FavoriteCreateDeleteView(APIView):
    permission_classes = [IsAuthenticated, ]
    pagination_class = None

    def get(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        user = self.request.user
        fav, created = Favorite.objects.get_or_create(user=user)
        if not created:
            if Favorite.objects.filter(user=user, recipe=recipe).exists():
                return Response(data='Этот рецепт уже есть в избранном')
            fav.recipe.add(recipe)
        fav.recipe.add(recipe)
        recipe_serializer = FavoriteRecipeViewSerializer(recipe)
        return Response(recipe_serializer.data, status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        user = self.request.user
        favorite = Favorite.objects.get(user=user)
        favorite.recipe.remove(recipe)
        return Response(status.HTTP_204_NO_CONTENT)


class CardAddDeleteRecipeView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        user = self.request.user
        cart, created = ShoppingCard.objects.get_or_create(user=user)
        if not created:
            if ShoppingCard.objects.filter(user=user, recipe=recipe).exists():
                return Response(data='Этот рецепт уже есть в корзине')
            cart.recipe.add(recipe)
        cart.recipe.add(recipe)
        recipe_serializer = FavoriteRecipeViewSerializer(recipe)
        return Response(recipe_serializer.data, status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        user = self.request.user
        card = ShoppingCard.objects.get(user=user)
        card.recipe.remove(recipe)
        return Response(status.HTTP_204_NO_CONTENT)


class DownloadShoppingCartView(APIView):
    def get(self, request):
        table = PrettyTable()
        table.field_names = ['Ингредиент', 'кол-во', 'ед-ца']
        ingredients_in_cart = Recipe.objects.filter(
            card_recipe__user=request.user).order_by(
            'ingredients__name__name').values(
            'ingredients__name__name',
            'ingredients__name__measurement_unit').annotate(
            total=Sum('ingredients__amount'))
        for item in ingredients_in_cart:
            table.add_row([item['ingredients__name__name'],
                           item['total'],
                           item['ingredients__name__measurement_unit']
                           ]
                          )
        file_data = table
        filename = 'ingredients.txt'
        response = HttpResponse(file_data, content_type='text/plain')
        response[
            'Content-Disposition'] = ('attachment; '
                                      'filename={0}'.format(filename))
        return response
