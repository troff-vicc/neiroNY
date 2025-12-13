from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import base64
from django.conf import settings
import os


@method_decorator(csrf_exempt, name='dispatch')
class ChatViewSet(viewsets.ViewSet):
    """
    ViewSet для обработки запросов генерации видео
    """
    
    def __init__(self, *args, **kwargs):
        self.api_key = settings.API_KEY
        super().__init__(*args, **kwargs)
    
    @action(detail=False, methods=['post'], url_path='generate')
    def generate(self, request):
        try:
            data = request.data
            
            prompt = data.get('prompt')
            
            
            #video_bytes = generate_video_from_text(
            #    prompt=prompt,
            #    api_key=self.api_key
            #)
            
            file_path = os.path.join(settings.MEDIA_ROOT, "1.mp4")
            with open(file_path, 'rb') as f:
                video_bytes = f.read()
            
            video_base64 = base64.b64encode(video_bytes).decode('utf-8')
            
            response_data = {
                'status': 'success',
                'message': 'Видео успешно сгенерировано',
                'video_data': video_base64,
                'format': 'base64',
                'prompt': prompt,
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
        
        except json.JSONDecodeError:
            return Response(
                {'error': 'Невалидный JSON формат'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except ImportError as e:
            return Response(
                {'error': 'Модуль генерации видео недоступен'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        except Exception as e:
            return Response(
                {
                    'error': 'Внутренняя ошибка сервера',
                    'details': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    