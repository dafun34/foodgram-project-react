from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import User, Subscriptions
from djoser.serializers import UserSerializer, UserCreateSerializer


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
        result = Subscriptions.objects.filter(user=obj, author=user).exists()
        return result


class SubscriptionsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriptions
        fields = ('author', 'user')

class SubscribeCreateSerializer(serializers.ModelSerializer):
    email = serializers.SlugRelatedField(queryset=User.objects.all(),
                                         slug_field='email')
    class Meta:
        model = Subscriptions
        fields = ('email',)




