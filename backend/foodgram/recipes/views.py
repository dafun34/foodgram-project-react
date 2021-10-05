from django.shortcuts import render
from rest_framework import viewsets
from .models import Recipe, Tag, Components
from .serializers import RecipeSerializer, TagSerializer, ComponentsSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class ComponentsViewSet(viewsets.ModelViewSet):
    queryset = Components.objects.all()
    serializer_class = ComponentsSerializer
