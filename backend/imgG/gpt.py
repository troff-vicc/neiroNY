# gpt.py
import openai
import base64
import requests
from django.conf import settings
from django.apps import apps


class DalleImageGenerator:
    def __init__(self):
        """Инициализация клиента OpenAI для DALL-E"""
        self.client = openai.OpenAI(api_key=settings.API_KEY)
        
    def get_template_data(self, template_name):
        """Получает данные шаблона из БД"""
        try:
            CardTemplate = apps.get_model('imgG', 'CardTemplate')
            template = CardTemplate.objects.filter(title=template_name).first()
            
            if template:
                data = {
                    'prompt': template.prompt if template.prompt else "",
                    'title': template.title,
                }
                
                return data
            else:
                return {}
        
        except Exception as e:
            return {}
        
    def description_img(self, bytes_image_string, file_type_name):
        mime_type = f"image/{file_type_name}"
        base64_image_string = base64.b64encode(bytes_image_string).decode('utf-8')
        image_data_url = f"data:{mime_type};base64,{base64_image_string}"
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",  # Рекомендуемая модель для Vision задач
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                # Промт для генерации описания для дальнейшего использования
                                "text": """"Подробно опиши (ОЧЕНЬ ВАЖНО ПОДРОБНО ОПИСАТЬ ЛЮДЕЙ НА ИЗОБРАЖЕНИЕ) это изображение.
                                 Используй богатый и детализированный язык, чтобы сгенерировать описание,
                                  которое может быть использовано для дальнейшей генерации нового изображения в DALLE.
                                   Укажи ключевые объекты (опиши заметные детали (например очки))"""
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    # Передаем Base64 в виде data URL
                                    "url": image_data_url,
                                    "detail": "auto"  # Запрос на более детальный анализ
                                }
                            }
                        ]
                    }
                ],
                max_tokens=200  # Ограничение длины ответа
            )
            
            image_description = response.choices[0].message.content
            print(image_description)
            print()
            return image_description
        
        except Exception as e:
            print(f"❌ Произошла ошибка при вызове OpenAI API: {e}")
    
    def generate_dalle3_image(self, prompt, size="1024x1024", quality="standard"):
        """Генерирует изображение через DALL-E 3"""
        try:
            print(prompt)
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality=quality,
                n=1,
                response_format="url"
            )
            
            image_url = response.data[0].url
            
            result = self._download_and_encode_image(image_url, prompt, model='dall-e-3')
            
            if result.get('success'):
                result['operation'] = 'generation'
                result['model'] = 'dall-e-3'
            
            return result
        
        except openai.OpenAIError as e:
            return {'success': False, 'error': f'DALL-E 3 error: {str(e)}'}
    
    def _download_and_encode_image(self, image_url, prompt=None, model=None):
        """Скачивает и кодирует изображение"""
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            img_response = requests.get(image_url, headers=headers, timeout=30)
            
            if img_response.status_code == 200:
                image_data = img_response.content
                
                # Определяем формат
                if image_data[:8] == b'\x89PNG\r\n\x1a\n':
                    img_format = 'png'
                elif image_data[:3] == b'\xff\xd8\xff':
                    img_format = 'jpeg'
                else:
                    img_format = 'png'
                
                image_b64 = base64.b64encode(image_data).decode('utf-8')
                
                result = {
                    'success': True,
                    'image_base64': image_b64,
                    'image_url': image_url,
                    'image_format': f'image/{img_format}',
                    'size_bytes': len(image_data)
                }
                
                if prompt:
                    result['prompt'] = prompt
                if model:
                    result['model'] = model
                
                return result
            else:
                return {'success': False, 'error': f'Download failed: HTTP {img_response.status_code}'}
        
        except Exception as e:
            return {'success': False, 'error': f'Download error: {str(e)}'}
    
    def process_image_generation(self, template_type, user_text=None, user_image_data=None, size=None, image_format=None):
        """Основная функция генерации"""
        try:
            # Получаем данные шаблона
            template_data = self.get_template_data(template_type)
            base_prompt = template_data.get('prompt', '')
            final_size = size
            
            descriptions = self.description_img(user_image_data, image_format)
            
            # Формируем промпт
            final_prompt = base_prompt
            if user_text and user_text.strip():
                final_prompt = f"{base_prompt} Дополнительные условия: {user_text}, описание: {descriptions}"
            
            # Выбираем стратегию
            
            result = self.generate_dalle3_image(
                prompt=final_prompt,
                size=final_size
            )

            # Добавляем метаданные
            if result.get('success'):
                result.update({
                    'template_type': template_type,
                    'template_title': template_data.get('title', template_type),
                    'size': final_size,
                    'prompt_used': final_prompt
                })
            
            return result
        
        except Exception as e:
            return {
                'success': False,
                'error': f'Processing error: {str(e)}',
                'template_type': template_type
            }


# Глобальный экземпляр
image_generator = DalleImageGenerator()


def process_with_gpt(template_type, text, image_data=None, image_format=None):
    """
    Интерфейсная функция для ViewSet
    """
    return image_generator.process_image_generation(
        template_type=template_type,
        user_text=text,
        user_image_data=image_data,
        image_format=image_format,
        size="1024x1024"
    )