from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.serializers import CustomUserSerializer

from .models import (Components, Favorite, Ingredients, Recipe, ShoppingCard,
                     Tag)


class TagListCreateDelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id',
                  'name',
                  'color',
                  'slug')


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id',
                  'name',
                  'color',
                  'slug', )

    def to_internal_value(self, data):
        try:
            Tag.objects.get(id=data)
        except ObjectDoesNotExist:
            raise serializers.ValidationError('Problem with tags id')
        return Tag.objects.get(id=data)


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ('id',
                  'name',
                  'measurement_unit')


class ComponentsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='name.id')
    name = serializers.ReadOnlyField(source='name.name')
    measurement_unit = serializers.ReadOnlyField(
        source='name.measurement_unit')

    class Meta:
        model = Components
        fields = ('id',
                  'name',
                  'amount',
                  'measurement_unit')


class ComponentsCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='name.id')

    class Meta:
        model = Components
        fields = ('id',
                  'amount')


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    tags = TagsSerializer(many=True)
    ingredients = ComponentsSerializer(source='component', many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id',
                  'tags',
                  'author',
                  'ingredients',
                  'is_favorited',
                  'is_in_shopping_cart',
                  'name',
                  'image',
                  'text',
                  'cooking_time',
                  )

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        user = request.user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        user = request.user
        if user.is_anonymous:
            return False
        else:
            return ShoppingCard.objects.filter(user=user, recipe=obj).exists()

    @transaction.atomic
    def create(self, validated_data):
        ingredients_data = validated_data.pop('component')
        tags = validated_data.pop('tags')
        request = self.context.get('request')
        user = request.user
        recipe = Recipe.objects.create(author=user, **validated_data)
        recipe.tags.add(*tags)
        components = []
        for ingredient in ingredients_data:
            some_compo = dict(ingredient)
            ingredient = some_compo['name']
            components.append(Components(
                name=Ingredients.objects.get(pk=ingredient['id']),
                amount=some_compo['amount'],
                component_in_recipe=recipe
            )
            )
        compo = Components.objects.bulk_create(components)
        recipe.ingredients.add(*compo)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('component')
        tags = validated_data.pop('tags')
        for item in validated_data:
            if Recipe._meta.get_field(item):
                setattr(instance, item, validated_data[item])
        instance.tags.clear()
        instance.tags.add(*tags)

        Components.objects.filter(component_in_recipe=instance).delete()
        components = []
        for ingredient in ingredients_data:
            some_compo = dict(ingredient)
            ingredient = some_compo['name']
            amount = some_compo['amount']
            components.append(Components(
                name=Ingredients(pk=ingredient['id']),
                amount=amount,
                component_in_recipe=instance)
            )
        Components.objects.bulk_create(components)
        instance.save()
        return instance


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
                message='???????? ???????????? ?????? ???????? ?? ?????? ?? ??????????????'
            )
        ]
