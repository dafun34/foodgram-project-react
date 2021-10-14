from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import User
from .models import Subscriptions
from djoser.serializers import UserCreateSerializer
from djoser.serializers import UserCreateSerializer
from rest_framework import validators


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed',)

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        user = request.user
        result = False
        if user.is_anonymous:
            return result
        else:
            result = Subscriptions.objects.filter(user=obj, author=user).exists()
        return result


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:

        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


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




