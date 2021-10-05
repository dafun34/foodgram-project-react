from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Recipe, Ingredients, Tag, Components

class ComponentsSerializer(serializers.ModelSerializer):
    ingredients = serializers.StringRelatedField()
    class Meta:
        model = Components
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = ComponentsSerializer(many=True, read_only=True)
    author = UserSerializer()
    class Meta:
        model = Recipe
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', 'color', 'slug')

