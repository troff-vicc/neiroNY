from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout

from .serializers import UserSerializer, UserCreateSerializer, UserLoginSerializer


class UserViewSet(viewsets.ViewSet):
    """
    ViewSet для работы с пользователями
    """
    
    def get_permissions(self):
        """
        Настройка разрешений
        """
        if self.action in ['register', 'login']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        """
        Регистрация нового пользователя
        """
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Создаем токен для нового пользователя
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                "message": "Пользователь успешно создан",
                "user": UserSerializer(user).data,
                "token": token.key
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        """
        Вход пользователя
        """
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        # Аутентификация пользователя
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            # Создаем или получаем токен
            token, created = Token.objects.get_or_create(user=user)
            
            # Логиним пользователя (опционально, для сессий)
            login(request, user)
            
            return Response({
                "message": "Вход выполнен успешно",
                "user": UserSerializer(user).data,
                "token": token.key
            })
        else:
            return Response(
                {"error": "Неверный email или пароль"},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['post'], url_path='logout')
    def logout(self, request):
        """
        Выход пользователя
        """
        if request.user.is_authenticated:
            # Удаляем токен
            Token.objects.filter(user=request.user).delete()
            logout(request)
            
            return Response({
                "message": "Выход выполнен успешно"
            })
        
        return Response(
            {"error": "Пользователь не авторизован"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        """
        Получить информацию о текущем пользователе
        """
        if request.user.is_authenticated:
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        
        return Response(
            {"error": "Пользователь не авторизован"},
            status=status.HTTP_401_UNAUTHORIZED
        )