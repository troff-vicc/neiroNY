from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
from ..gpt import GPTClient
import uuid


class ChatViewSet(viewsets.ViewSet):
    """
    ViewSet для обработки чата с GPT
    """
    def __init__(self, *args, **kwargs):
        api_key = settings.API_KEY
        super().__init__(*args, **kwargs)
        self.gpt_client = GPTClient(
            api_key=api_key
        )
    
    @action(detail=False, methods=['post'], url_path='generate')
    def generate(self, request):
        """
        Основная функция генерации поздравления или сценария
        """
        try:
            message = request.data.get('message')
            session_id = request.data.get('session_id', str(uuid.uuid4()))
            
            if not message:
                return Response(
                    {'error': 'Сообщение не может быть пустым'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            response_text = self.gpt_client.send_message(
                message=message,
                session_id=session_id
            )
            
            return Response({
                'success': True,
                'response': response_text,
                'user_message': message,
                'session_id': session_id
            })
        
        except Exception as e:
            return Response(
                {'error': f'Ошибка при генерации: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'], url_path='regenerate')
    def regenerate(self, request):
        """
        Функция для переделки текста
        """
        try:
            message = request.data.get('message')
            session_id = request.data.get('session_id', str(uuid.uuid4()))
            
            if not message:
                return Response(
                    {'error': 'Сообщение не может быть пустым'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            response_text = self.gpt_client.regenerate_text(
                message=message,
                session_id=session_id
            )
            
            return Response({
                'success': True,
                'response': response_text,
                'user_message': message,
                'session_id': session_id
            })
        
        except Exception as e:
            return Response(
                {'error': f'Ошибка при переделке: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'], url_path='clear-history')
    def clear_history(self, request):
        """
        Очистка истории сообщений
        """
        try:
            session_id = request.data.get('session_id')
            self.gpt_client.clear_history(session_id)
            
            return Response({
                'success': True,
                'message': 'История очищена',
                'session_id': session_id if session_id else 'all'
            })
        
        except Exception as e:
            return Response(
                {'error': f'Ошибка при очистке истории: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )