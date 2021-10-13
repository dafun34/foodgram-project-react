from rest_framework import serializers
from .models import User, Subscriptions
from djoser.serializers import UserSerializer, UserCreateSerializer


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',)


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




