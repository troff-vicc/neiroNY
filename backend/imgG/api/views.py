from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import base64
from ..gpt import process_with_gpt  # Импортируем готовую функцию


class CardTemplateViewSet(viewsets.ViewSet):
    
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
            
            
            # Подготавливаем данные для внешней функции
            gpt_params = {
                'template_type': template_type,
                'text': text,
                'image_data': None,
                'image_format': None
            }
            
            try:
                image_data = base64.b64decode(request.data['image_data'])
                gpt_params['image_format'] = request.data.get('image_format', 'image/jpeg')
            except (base64.binascii.Error, ValueError) as e:
                return Response(
                    {'error': f'Invalid base64 image: {str(e)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Сохраняем бинарные данные изображения если есть
            if image_data:
                gpt_params['image_data'] = image_data
            
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
                'message': result.get('content'),
            }
            
            # Если в результате есть сгенерированное изображение (base64)
            if 'image_base64' in result:
                response_data['generated_image'] = result['image_base64']
                response_data['image_format'] = result.get('image_format', 'image/png')
                response_data['image_size'] = result.get('size_bytes', 0)
            
            if 'image_url' in result:
                response_data['image_url'] = result['image_url']
            
            return Response(response_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': f'Internal server error: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )