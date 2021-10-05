from django.shortcuts import render
from rest_framework import viewsets
from .models import Recipe, Tag
from .serializers import RecipeSerializer, TagSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
