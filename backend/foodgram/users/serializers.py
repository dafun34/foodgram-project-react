from rest_framework import serializers
from .models import User, Subscriptions
from djoser.serializers import UserSerializer, UserCreateSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ( 'id', 'username', 'email', 'first_name', 'last_name')



class SubscriptionsSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Subscriptions
        fields = ('author',)



