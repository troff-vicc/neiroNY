from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Модель пользователя"""
    
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    # Убираем стандартные поля, чтобы избежать конфликта
    groups = None
    user_permissions = None
    
    def __str__(self):
        return f"User: {self.email}"