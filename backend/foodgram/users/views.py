from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from .serializers import UserSerializer, SubscriptionsSerializer
from .models import User, Subscriptions
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'head', 'patch', 'delete']


class SubscriptionsList(viewsets.ModelViewSet):

    def list(self, request):
        user = self.request.user
        queryset = Subscriptions.objects.filter(user=user)
        serializer = SubscriptionsSerializer(queryset, many=True)
        return Response(serializer.data)




