from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .models import User
from .views import UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls))
]