from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CardTemplateViewSet

img_router = DefaultRouter()
img_router.register(r'img', CardTemplateViewSet, basename='img')

urlpatterns = [
    path('', include(img_router.urls)),
]