from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ChatViewSet

video_router = DefaultRouter()
video_router.register(r'video', ChatViewSet, basename='video')
