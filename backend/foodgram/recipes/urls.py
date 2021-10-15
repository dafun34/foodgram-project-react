from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (RecipeViewSet,
                    ComponentsViewSet,
                    IngredientsViewSet,
                    TagsViewSet,
                    FavoriteCreate,
                    CardAddRecipeView)

router = DefaultRouter()
router.register('recipes', RecipeViewSet, basename='recipe')
router.register('tags', TagsViewSet, basename='tag')
router.register('components', ComponentsViewSet, basename='components')
router.register('ingredients', IngredientsViewSet, basename='ingredients')


urlpatterns = [
    path('recipes/<int:recipe_id>/shopping_card/', CardAddRecipeView.as_view(), name='add_recipe_to_card'),
    path('recipes/<int:recipe_id>/favorite/', FavoriteCreate.as_view(), name='favorite_create'),
    path('', include(router.urls))
]