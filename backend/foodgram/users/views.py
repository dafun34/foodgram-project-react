from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, \
    ListModelMixin
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .serializers import UserSerializer, SubscriptionsSerializer, SubscribeCreateSerializer
from .models import User, Subscriptions
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

class CreateListDestroyViewSet(ListModelMixin,
                               CreateModelMixin,
                               DestroyModelMixin,
                               GenericViewSet):
    pass

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SubscriptionsList(viewsets.ModelViewSet):

    def list(self, request):
        user = self.request.user
        queryset = Subscriptions.objects.filter(user=user)
        serializer = SubscriptionsSerializer(queryset, many=True)
        return Response(serializer.data)


class SubscriptionsCreate(viewsets.ModelViewSet):
    http_method_names = ['get', 'delete']
    queryset = Subscriptions.objects.all()
    serializer_class = SubscriptionsSerializer

    def list(self,request, user_id):
        user = self.request.user
        user_id = self.kwargs.get('user_id')
        author = get_object_or_404(User, id=user_id)
        subscribe = Subscriptions.objects.create(user=user, author=author)
        serializer = UserSerializer(author)
        return Response(serializer.data)

    def destroy(self, request, user_id):
        user = self.request.user
        user_id = self.kwargs.get('user_id')


