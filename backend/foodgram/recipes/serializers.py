from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.request import Request
from users.models import User
from users.serializers import UserSerializer
from .models import Recipe, Ingredients, Components, Tag, Favorite
from drf_extra_fields.fields import Base64ImageField


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id',
                  'name',
                  'color',
                  'slug')



class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ('id',
                  'name',
                  'measurement_unit')


class ComponentsListSerializer(serializers.ModelSerializer):
    ingredient = serializers.StringRelatedField()
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = Components
        fields = ('id',
                  'ingredient',
                  'amount',
                  'measurement_unit')

class ComponentsCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')

    class Meta:
        model = Components
        fields = ('id',
                  'amount')



class RecipeListSerializer(serializers.ModelSerializer):
    ingredients = ComponentsListSerializer(many=True)
    author = UserSerializer()
    tag = TagsSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id',
                  'tag',
                  'author',
                  'ingredients',
                  'is_favorited',
                  'name',
                  'image',
                  'text',
                  'cooking_time',
                  )
    def get_is_favorited(self,obj):
        author = obj.author.id
        request = self.context.get('request')
        user = request.user
        result = Favorite.objects.filter(user=user,recipe=obj).exists()
        return result




class RecipeCreateSerializer(serializers.ModelSerializer):
    """ здесь переопределить сериалайзер на кастомный(serializers.Serializer)"""
    image = Base64ImageField()
    tag = serializers.SlugRelatedField(queryset=Tag.objects.all(),
                                       slug_field='id', many=True)
    ingredients = ComponentsCreateSerializer(source='component', many=True)
    is_favorited = serializers.SerializerMethodField()
    class Meta:
        model = Recipe
        fields = ('id',
                  'tag',
                  'author',
                  'ingredients',
                  'name',
                  'image',
                  'text',
                  'cooking_time',
                  'is_favorited',)

    def get_is_favorited(self, obj):
        return str(obj.id)

    def create(self, validated_data):
        ingredients_data = validated_data.pop('component')
        tags = validated_data.pop('tag')
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags:
            recipe.tag.add(tag)
        for ingredient in ingredients_data:
            some_compo = dict(ingredient)
            ingredient = some_compo['ingredient']
            component = Components.objects.create(
                ingredient=Ingredients.objects.get(pk=ingredient['id']),
                amount=some_compo['amount'],
                component_in_recipe=recipe
            )
            recipe.ingredients.add(component)
        return recipe


class FavoriteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('user', 'recipe')