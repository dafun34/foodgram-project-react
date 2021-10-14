from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .models import User
from .views import SubscriptionsList, SubscribeCreate

router = DefaultRouter()




urlpatterns = [
    path('', include('djoser.urls')),
    path('users/<int:user_id>/subscribe/', SubscribeCreate.as_view(), name='subscribe'),
    path('users/subscriptions/', SubscriptionsList.as_view()),
    path('auth/', include('djoser.urls.authtoken')),


]
