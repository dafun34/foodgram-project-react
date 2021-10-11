from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (RecipeViewSet,
                    ComponentsViewSet,
                    IngredientsViewSet,
                    TagsViewSet)

router = DefaultRouter()
router.register('recipes', RecipeViewSet, basename='recipe')
router.register('tags', TagsViewSet, basename='tag')
router.register('components', ComponentsViewSet, basename='components')
router.register('ingredients', IngredientsViewSet, basename='ingredients')


urlpatterns = [
    path('', include(router.urls))
]