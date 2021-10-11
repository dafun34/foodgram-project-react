from rest_framework import serializers
from users.serializers import UserSerializer
from .models import Recipe, Ingredients, Components, Tag
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

    class Meta:
        model = Recipe
        fields = ('id',
                  'tag',
                  'author',
                  'ingredients',
                  'name',
                  'image',
                  'text',
                  'cooking_time')


class RecipeCreateSerializer(serializers.ModelSerializer):
    """ здесь переопределить сериалайзер на кастомный(serializers.Serializer)"""
    image = Base64ImageField()
    tag = serializers.SlugRelatedField(queryset=Tag.objects.all(),
                                       slug_field='id', many=True)
    ingredients = ComponentsCreateSerializer(source='component', many=True)
    class Meta:
        model = Recipe
        fields = '__all__'

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

