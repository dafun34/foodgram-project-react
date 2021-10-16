from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.validators import UniqueTogetherValidator

from users.models import User
from users.serializers import UserSerializer
from .models import Recipe, Ingredients, Components, Tag, Favorite, ShoppingCard
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
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id',
                  'tag',
                  'author',
                  'ingredients',
                  'is_favorited',
                  'is_in_shopping_cart',
                  'name',
                  'image',
                  'text',
                  'cooking_time',
                  )

    def get_is_favorited(self,obj):
        author = obj.author.id
        request = self.context.get('request')
        user = request.user
        result = False
        if user.is_anonymous:
            return result
        else:
            result = Favorite.objects.filter(user=user, recipe=obj).exists()
        return result

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        user = request.user
        result = False
        if user.is_anonymous:
            return result
        else:
            result = ShoppingCard.objects.filter(user=user, recipe=obj).exists()
            return result


class RecipeCreateSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    tag = serializers.SlugRelatedField(queryset=Tag.objects.all(),
                                       slug_field='id', many=True)
    ingredients = ComponentsCreateSerializer(source='component', many=True)

    class Meta:
        model = Recipe
        fields = ('id',
                  'tag',
                  'author',
                  'ingredients',
                  'name',
                  'image',
                  'text',
                  'cooking_time',)

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

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('component')
        tags = validated_data.pop('tag')
        for item in validated_data:
            if Recipe._meta.get_field(item):
                setattr(instance, item, validated_data[item])
        instance.tag.clear()
        for tag in tags:
            instance.tag.add(tag)

        Components.objects.filter(component_in_recipe=instance).delete()
        for ingredient in ingredients_data:
            some_compo = dict(ingredient)
            ingredient = some_compo['ingredient']
            amount = some_compo['amount']
            component = Components.objects.create(
                ingredient=Ingredients.objects.get(pk=ingredient['id']),
                amount=amount,
                component_in_recipe=instance
            )
            instance.ingredients.add(component)
        instance.save()
        return instance


class FavoriteCreateSerializer(serializers.ModelSerializer):
    recipe = RecipeListSerializer(many=True)
    class Meta:
        model = Favorite
        fields = ('user',
                  'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=['recipe', 'user'],
                message='Этот рецепт уже есть у вас в избранном'
            )
        ]





class FavoriteRecipeViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id',
                  'name',
                  'image',
                  'cooking_time')


class ShoppingCardAddRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCard
        fields = ('user',
                  'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCard.objects.all(),
                fields=['recipe', 'user'],
                message='Этот рецепт уже есть у вас в корзине'
            )
        ]

class ShoppCard_TEST_Serializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    cooking_time = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingCard
        fields = ('id',
                  'name',
                  'image',
                  'cooking_time')

    validators = [
        UniqueTogetherValidator(
            queryset=ShoppingCard.objects.all(),
            fields=['recipe', 'user'],
            message='Этот рецепт уже есть у вас в корзине'
        )
    ]



    def get_id(self, obj):
        return obj.id

    def get_name(self, obj):
        return obj.name

    def get_image(self, obj):
        return obj.image.url

    def get_cooking_time(self, obj):
        return obj.cooking_time

