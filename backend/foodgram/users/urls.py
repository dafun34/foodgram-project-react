from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import SubscriptionsList, SubscribeCreate, HomeUserListView

router = DefaultRouter()

urlpatterns = [
    path('users/<int:user_id>/subscribe/', SubscribeCreate.as_view(),
         name='subscribe'),
    path('users/subscriptions/', SubscriptionsList.as_view()),
    path('users/me/', HomeUserListView.as_view()),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),


]
