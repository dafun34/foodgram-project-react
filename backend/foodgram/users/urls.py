from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .models import User
from .views import UserViewSet, SubscriptionsList, SubscriptionsCreate

router = DefaultRouter()

router.register('users', UserViewSet, basename='users')

subscriptions_list = SubscriptionsList.as_view({'get': 'list'})
subscriptions_create = SubscriptionsList.as_view({'get': 'create',
                                                  'delete': 'destroy'})
router.register(
    r'users/(?P<user_id>[0-9]+)/subscribe',
    SubscriptionsCreate,
    basename='subscribe'
)
urlpatterns = [
    path('users/subscriptions/', subscriptions_list),
    path('', (include(router.urls))),
    path('auth/', include('djoser.urls.authtoken')),

]
