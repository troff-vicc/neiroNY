from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import base64
import tempfile
import os
from django.conf import settings
from ..gpt import process_with_gpt  # Импортируем готовую функцию


class ChatViewSet(viewsets.ViewSet):
    
    @method_decorator(csrf_exempt)
    @action(detail=False, methods=['post'], url_path='generate')
    def send_message(self, request):
        """
        Принимает данные, вызывает внешнюю функцию и возвращает результат
        """
        try:
            # Получаем данные из запроса
            template_type = request.data.get('template_type')
            text = request.data.get('text', '')
            
            # Проверяем обязательные поля
            if not template_type:
                return Response(
                    {'error': 'template_type is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Подготавливаем данные для внешней функции
            gpt_params = {
                'template_type': template_type,
                'text': text,
                'image_data': None,
                'image_format': None
            }
            
            # Обрабатываем изображение если есть
            image_file = None
            image_data = None
            
            # 1. Изображение как файл (multipart/form-data)
            if 'image' in request.FILES:
                image_file = request.FILES['image']
                # Читаем файл в бинарном формате
                image_data = image_file.read()
                gpt_params['image_format'] = image_file.content_type
            
            # 2. Изображение как base64 строка
            elif 'image' in request.data and isinstance(request.data['image'], str):
                try:
                    image_data = base64.b64decode(request.data['image'])
                    gpt_params['image_format'] = request.data.get('image_format', 'image/jpeg')
                except (base64.binascii.Error, ValueError) as e:
                    return Response(
                        {'error': f'Invalid base64 image: {str(e)}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # 3. Изображение как URL
            elif 'image_url' in request.data:
                gpt_params['image_url'] = request.data['image_url']
            
            # Сохраняем бинарные данные изображения если есть
            if image_data:
                gpt_params['image_data'] = image_data
            
            # Вызываем внешнюю функцию обработки с GPT
            # Предполагаем, что process_with_gpt возвращает словарь с результатом
            result = process_with_gpt(**gpt_params)
            
            # Проверяем результат
            if not result or 'error' in result:
                error_msg = result.get('error', 'Unknown error from GPT processing')
                return Response(
                    {'error': error_msg},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # Подготавливаем ответ
            response_data = {
                'success': True,
                'template_type': template_type,
                'user_input': {
                    'text': text,
                    'has_image': image_data is not None or 'image_url' in gpt_params
                },
                'generated_content': result.get('content'),
                'processing_info': result.get('info', {})
            }
            
            # Если в результате есть сгенерированное изображение (base64)
            if 'generated_image' in result:
                response_data['generated_image'] = result['generated_image']
                response_data['image_format'] = result.get('image_format', 'image/png')
            
            return Response(response_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': f'Internal server error: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )