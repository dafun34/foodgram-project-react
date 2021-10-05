from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .models import Recipe
from .views import RecipeViewSet, TagViewSet, ComponentsViewSet

router = DefaultRouter()
router.register('recipes', RecipeViewSet, basename='recipe')
router.register('tags', TagViewSet, basename='tag')
router.register('components', ComponentsViewSet, basename='components')

urlpatterns = [
    path('', include(router.urls))
]