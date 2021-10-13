from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .models import User
from .views import UserViewSet, SubscriptionsList, SubscribeCreate

router = DefaultRouter()

router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('users/<int:user_id>/subscribe/', SubscribeCreate.as_view(), name='subscribe'),
    path('users/subscriptions/', SubscriptionsList.as_view()),
    path('', (include(router.urls))),
    path('auth/', include('djoser.urls.authtoken')),

]
