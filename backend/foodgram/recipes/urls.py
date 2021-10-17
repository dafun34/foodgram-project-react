from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (RecipeViewSet,
                    ComponentsViewSet,
                    IngredientsViewSet,
                    TagsViewSet,
                    FavoriteCreateDeleteView,
                    CardAddDeleteRecipeView, DownloadShoppingCartView)

router = DefaultRouter()
router.register('recipes', RecipeViewSet, basename='recipe')
router.register('tags', TagsViewSet, basename='tag')
router.register('components', ComponentsViewSet, basename='components')
router.register('ingredients', IngredientsViewSet, basename='ingredients')


urlpatterns = [
    path('recipes/download_shopping_cart/', DownloadShoppingCartView.as_view(),name='download_shopping_cart'),
    path('', include(router.urls)),

    path('recipes/<int:recipe_id>/favorite/',
         FavoriteCreateDeleteView.as_view(),
         name='favorite_create'),

    path('recipes/<int:recipe_id>/shopping_cart/',
         CardAddDeleteRecipeView.as_view(),
         name='add_recipe_to_card'),

]