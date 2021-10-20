from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.core.exceptions import ObjectDoesNotExist
from users.serializers import UserSerializer, CustomUserCreateSerializer, CustomUserSerializer
from .models import (Recipe,
                     Ingredients,
                     Components,
                     Tag,
                     Favorite,
                     ShoppingCard)
from drf_extra_fields.fields import Base64ImageField


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
            tag = Tag.objects.get(id=data)
        except ObjectDoesNotExist:
            raise serializers.ValidationError('Problem with tags id')
        return tag


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ('id',
                  'name',
                  'measurement_unit')


# class ComponentSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(source='ingredient.id')
#     name = serializers.ReadOnlyField(source='ingredient.name')
#     measurement_unit = serializers.ReadOnlyField( source='ingredient.measurement_unit' )
#     class Meta:
#         model = Components
#         fields = ('id', 'name', 'measurement_unit', 'amount', )

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

#
# class RecipeListSerializer(serializers.ModelSerializer):
#     image = Base64ImageField()
#     tags = TagsSerializer(many=True)
#     ingredients = ComponentsSerializer(source='component', many=True)
#     is_favorited = serializers.SerializerMethodField()
#     is_in_shopping_cart = serializers.SerializerMethodField()
#     author = UserSerializer(required=False)
#
#     class Meta:
#         model = Recipe
#         fields = ('id',
#                   'tags',
#                   'author',
#                   'ingredients',
#                   'is_favorited',
#                   'is_in_shopping_cart',
#                   'name',
#                   'image',
#                   'text',
#                   'cooking_time',
#                   )
#
#     def get_is_favorited(self, obj):
#         request = self.context.get('request')
#         user = request.user
#         result = False
#         if user.is_anonymous:
#             return result
#         else:
#             result = Favorite.objects.filter(user=user, recipe=obj).exists()
#         return result
#
#     def get_is_in_shopping_cart(self, obj):
#         request = self.context.get('request')
#         user = request.user
#         result = False
#         if user.is_anonymous:
#             return result
#         else:
#             result = ShoppingCard.objects.filter(
#                 user=user, recipe=obj).exists()
#
#             return result
#

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
            result = ShoppingCard.objects.filter(
                user=user, recipe=obj).exists()

            return result

    def create(self, validated_data):
        ingredients_data = validated_data.pop('component')
        tags = validated_data.pop('tags')
        request = self.context.get('request')
        user = request.user
        recipe = Recipe.objects.create(author=user, **validated_data)
        for tag in tags:
            recipe.tags.add(tag)
        for ingredient in ingredients_data:
            some_compo = dict(ingredient)
            ingredient = some_compo['name']
            component = Components.objects.create(
                name=Ingredients.objects.get(pk=ingredient['id']),
                amount=some_compo['amount'],
                component_in_recipe=recipe
            )
            recipe.ingredients.add(component)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('component')
        tags = validated_data.pop('tags')
        for item in validated_data:
            if Recipe._meta.get_field(item):
                setattr(instance, item, validated_data[item])
        instance.tags.clear()
        for tag in tags:
            instance.tags.add(tag)

        Components.objects.filter(component_in_recipe=instance).delete()
        for ingredient in ingredients_data:
            some_compo = dict(ingredient)
            ingredient = some_compo['name']
            amount = some_compo['amount']
            component = Components.objects.create(
                name=Ingredients.objects.get(pk=ingredient['id']),
                amount=amount,
                component_in_recipe=instance
            )
            instance.ingredients.add(component)
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
                message='Этот рецепт уже есть у вас в корзине'
            )
        ]



# class RecipeSerializer(serializers.ModelSerializer):
#     tags = TagSerializer(many=True)
#     ingredients = ComponentSerializer(many=True)
#     author = CustomUserSerializer(read_only=True)
#     image = Base64ImageField(max_length=None, use_url=True)
#     is_favorited = serializers.SerializerMethodField()
#     is_in_shopping_cart = serializers.SerializerMethodField()
#     class Meta: model = Recipe fields = ('id',
#                                          'tags',
#                                          'author',
#                                          'ingredients',
#                                          'is_favorited',
#                                          'is_in_shopping_cart',
#                                          'name',
#                                          'image',
#                                          'text',
#                                          'cooking_time')
#     def get_is_favorited(self, obj):
#         if self.context['request'].user.is_anonymous:
#             return False
#         return Favorites.objects.filter( owner=self.context['request'].user, recipes=obj ).exists()
#         def get_is_in_shopping_cart(self, obj):
#             if self.context['request'].user.is_anonymous:
#                 return False
#             return ShoppingCart.objects.filter( owner=self.context['request'].user, recipes=obj ).exists()
#             @transaction.atomic
#             def create(self, validated_data):
#                 tags = validated_data.pop('tags')
#                 ingredients = validated_data.pop('ingredients')
#                 recipe = Recipe.objects.create(**validated_data, author=self.context['request'].user)
#                 for tag in tags:
#                     recipe.tags.add(tag)
#                 return add_ingredients(recipe, ingredients)
#
#                 @transaction.atomic
#                 def update(self, recipe, validated_data):
#                     tags = validated_data.pop('tags')
#                     ingredients = validated_data.pop('ingredients')
#                     recipe.name = validated_data.pop('name')
#                     recipe.text = validated_data.pop('text')
#                     if validated_data.get('image') is not None:
#                         recipe.image = validated_data.pop('image')
#                         recipe.cooking_time = validated_data.pop('cooking_time')
#                         recipe.save()
#                         recipe.tags.set(tags)
#                         recipe.ingredients.set('')
#                         return add_ingredients(recipe, ingredients)