from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Subscriptions, User
from .serializers import (CustomUserSerializer, SubscriptionsListSerializer,
                          UserSerializer)


class HomeUserListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class SubscriptionsList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(following__user=user)


class SubscribeCreate(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        data = {'user': request.user.id, 'author': user_id}
        serializer = SubscriptionsListSerializer(data=data,
                                                 context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        author = get_object_or_404(User, id=user_id)
        serializer_user = CustomUserSerializer(author,
                                               context={'request': request})
        return Response(serializer_user.data, status=status.HTTP_201_CREATED)

    def delete(self, request, user_id):
        user = request.user
        author = get_object_or_404(User, id=user_id)
        subscription = get_object_or_404(Subscriptions, user=user,
                                         author=author)
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
