from djoser.serializers import (UserCreateSerializer,
                                UserSerializer as djoserUser)
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from recipes.models import Recipe
from users.models import Subscriptions, User


class FavoriteRecipeViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id',
                  'name',
                  'image',
                  'cooking_time')


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed',
                  'recipes',
                  'recipes_count'
                  )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        user = request.user
        if user.is_anonymous:
            return False
        return Subscriptions.objects.filter(user=obj, author=user).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = request.query_params.get('recipes_limit')
        context = {'request': request}
        if recipes_limit is not None:
            recipes = obj.recipe.all()[:int(recipes_limit)]
        else:
            recipes = obj.recipe.all()
        serializer = FavoriteRecipeViewSerializer(data=recipes,
                                                  many=True,
                                                  context=context)
        serializer.is_valid()
        return serializer.data

    def get_recipes_count(self, obj):
        count = 0
        count += obj.recipe.count()
        return count


class SubscriptionsCustom(serializers.ModelSerializer):
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'recipes_count')

    def get_recipes_count(self):
        count = 0
        instance = self.instance
        for item in instance:
            count += item.recipe.count()
        return count


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


class CustomUserSerializer(djoserUser):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        user = request.user
        if user.is_anonymous:
            return False
        return Subscriptions.objects.filter(user=user, author=obj).exists()


class SubscriptionsListSerializer(serializers.ModelSerializer):
    def validate(self, data):
        request = self.context['request']
        user = request.user
        if data['author'] == user:
            raise serializers.ValidationError(
                'Пользователь не может подписаться сам на себя')
        return data

    class Meta:
        model = Subscriptions
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Subscriptions.objects.all(),
                fields=['author', 'user'],
                message='Это автор уже у вас в друзьях'
            )
        ]
