from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import HomeUserListView, SubscribeCreate, SubscriptionsList

router = DefaultRouter()

urlpatterns = [
    path('users/subscriptions/', SubscriptionsList.as_view()),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/<int:user_id>/subscribe/', SubscribeCreate.as_view(),
         name='subscribe'),

    path('users/me/', HomeUserListView.as_view()),


]
