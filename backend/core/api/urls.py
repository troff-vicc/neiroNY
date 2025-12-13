from rest_framework.routers import DefaultRouter
from textG.api.urls import text_router
from users.api.urls import users_router
from imgG.api.urls import img_router
from django.urls import path, include

router = DefaultRouter()


router.registry.extend(text_router.registry)
router.registry.extend(users_router.registry)
router.registry.extend(img_router.registry)

urlpatterns = [
    path('', include(router.urls)),
]