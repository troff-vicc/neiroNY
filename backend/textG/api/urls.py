from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ChatViewSet

text_router = DefaultRouter()
text_router.register(r'text', ChatViewSet, basename='text')