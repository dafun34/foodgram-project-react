from django.shortcuts import render
from rest_framework import generics, status, viewsets
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, \
    ListModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from .serializers import UserSerializer, SubscriptionsListSerializer, UserCreateSerializer, CustomUserCreateSerializer
from .models import User, Subscriptions
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404


class SubscriptionsList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(following__user=user)


class SubscribeCreate(APIView):
    def get(self, request, user_id):
        data = {'user': request.user.id, 'author': user_id}
        serializer = SubscriptionsListSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        author = get_object_or_404(User, id=user_id)
        serializer_user = UserSerializer(author, context={'request': request})
        return Response(serializer_user.data, status=status.HTTP_201_CREATED)

    def delete(self, request, user_id):
        user = request.user
        author = get_object_or_404(User, id=user_id)
        subscription = get_object_or_404(Subscriptions, user=user,
                                         author=author)
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)






