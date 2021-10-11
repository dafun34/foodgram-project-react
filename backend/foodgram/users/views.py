from django.shortcuts import render
from rest_framework import viewsets
from .serializers import UserSerializer, SubscriptionsSerializer
from .models import User, Subscriptions

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']


class FollowingViewSet(viewsets.ModelViewSet):
    queryset = Subscriptions.objects.all()
    serializer_class = SubscriptionsSerializer
