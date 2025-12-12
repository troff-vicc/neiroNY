from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

users_router = DefaultRouter()
users_router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(users_router.urls)),
]