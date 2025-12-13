# gpt.py
import openai
import base64
import io
import requests
import tempfile
from PIL import Image
from django.conf import settings
from django.apps import apps
import logging
import os

logger = logging.getLogger(__name__)


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
                    'default_size': getattr(template, 'default_size', '1024x1024')
                }
                
                if template.image:
                    data['image_path'] = template.image.path
                    data['image_url'] = template.image.url
                else:
                    data['image_path'] = None
                    data['image_url'] = None
                
                return data
            else:
                logger.warning(f"Template '{template_name}' not found")
                return self.get_default_template(template_name)
        
        except Exception as e:
            logger.error(f"Error fetching template: {str(e)}")
            return self.get_default_template(template_name)
    
    def get_default_template(self, template_name):
        """Стандартные шаблоны"""
        default_templates = {
            'greeting': {
                'prompt': 'Create a beautiful greeting card with warm colors and elegant typography',
                'title': 'greeting',
                'default_size': '1024x1024'
            },
            'congratulation': {
                'prompt': 'Design a congratulatory card with celebratory elements and golden accents',
                'title': 'congratulation',
                'default_size': '1024x1024'
            },
            'birthday': {
                'prompt': 'Create a festive birthday card with balloons, cake, and party elements',
                'title': 'birthday',
                'default_size': '1024x1024'
            },
            'business': {
                'prompt': 'Design a professional business card with clean layout and corporate style',
                'title': 'business',
                'default_size': '1024x1024'
            }
        }
        
        return default_templates.get(
            template_name.lower(),
            {
                'prompt': f'Create a beautiful card design for {template_name}',
                'title': template_name,
                'image_path': None,
                'image_url': None,
                'default_size': '1024x1024'
            }
        )
    
    def convert_to_rgba_png(self, image_bytes):
        """
        Конвертирует изображение в PNG с альфа-каналом (RGBA)

        Args:
            image_bytes (bytes): Исходные байты изображения

        Returns:
            bytes: PNG байты в формате RGBA
        """
        try:
            # Открываем изображение
            image = Image.open(io.BytesIO(image_bytes))
            
            logger.info(f"Original image: format={image.format}, mode={image.mode}, size={image.size}")
            
            # Конвертируем в RGBA (обязательно для DALL-E 2)
            if image.mode != 'RGBA':
                if image.mode == 'RGB':
                    # RGB -> RGBA (добавляем полностью непрозрачный альфа-канал)
                    rgba_image = Image.new('RGBA', image.size)
                    rgba_image.paste(image, (0, 0))
                    image = rgba_image
                elif image.mode in ('RGBA', 'LA', 'L', 'P', '1', 'CMYK'):
                    # Конвертируем через RGB
                    if image.mode in ('P', '1'):
                        image = image.convert('RGBA')
                    elif image.mode == 'CMYK':
                        image = image.convert('RGB')
                        rgba_image = Image.new('RGBA', image.size)
                        rgba_image.paste(image, (0, 0))
                        image = rgba_image
                    elif image.mode == 'LA':
                        # LA -> RGBA
                        rgb_image = image.convert('RGB')
                        rgba_image = Image.new('RGBA', rgb_image.size)
                        rgba_image.paste(rgb_image, (0, 0))
                        # Используем L-канал как альфа
                        alpha = image.getchannel('A') if 'A' in image.getbands() else image.getchannel('L')
                        rgba_image.putalpha(alpha)
                        image = rgba_image
                    elif image.mode == 'L':
                        # L -> RGBA
                        rgb_image = image.convert('RGB')
                        rgba_image = Image.new('RGBA', rgb_image.size)
                        rgba_image.paste(rgb_image, (0, 0))
                        image = rgba_image
            
            # Проверяем, что у нас теперь RGBA
            if image.mode != 'RGBA':
                logger.warning(f"Image mode is {image.mode}, forcing RGBA")
                image = image.convert('RGBA')
            
            # Сохраняем как PNG
            output = io.BytesIO()
            image.save(output, format='PNG', optimize=True)
            png_bytes = output.getvalue()
            
            # Проверяем сигнатуру
            if png_bytes[:8] == b'\x89PNG\r\n\x1a\n':
                logger.info(f"Successfully converted to RGBA PNG: {len(png_bytes)} bytes")
                return png_bytes
            else:
                # Принудительно сохраняем
                output = io.BytesIO()
                image.save(output, format='PNG')
                return output.getvalue()
        
        except Exception as e:
            logger.error(f"Error converting to RGBA PNG: {str(e)}")
            return None
    
    def create_square_rgba_image(self, rgba_bytes, size=512):
        """
        Создает квадратное изображение RGBA заданного размера

        Args:
            rgba_bytes (bytes): PNG байты в RGBA
            size (int): Размер стороны квадрата

        Returns:
            bytes: Квадратное PNG изображение
        """
        try:
            image = Image.open(io.BytesIO(rgba_bytes))
            
            # Проверяем режим
            if image.mode != 'RGBA':
                image = image.convert('RGBA')
            
            width, height = image.size
            
            # Если изображение уже квадратное и нужного размера
            if width == height and width == size:
                output = io.BytesIO()
                image.save(output, format='PNG', optimize=True)
                return output.getvalue()
            
            # Создаем новое квадратное изображение
            square_image = Image.new('RGBA', (size, size), (0, 0, 0, 0))  # Прозрачный фон
            
            # Рассчитываем положение для вставки
            if width > height:
                # Широкое изображение
                new_width = size
                new_height = int(size * height / width)
                y_offset = (size - new_height) // 2
                x_offset = 0
            else:
                # Высокое изображение
                new_height = size
                new_width = int(size * width / height)
                x_offset = (size - new_width) // 2
                y_offset = 0
            
            # Изменяем размер с сохранением пропорций
            resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Вставляем в центр
            square_image.paste(resized_image, (x_offset, y_offset))
            
            # Сохраняем
            output = io.BytesIO()
            square_image.save(output, format='PNG', optimize=True)
            
            result_bytes = output.getvalue()
            logger.info(f"Created square image: {size}x{size}, {len(result_bytes)} bytes")
            return result_bytes
        
        except Exception as e:
            logger.error(f"Error creating square image: {str(e)}")
            return rgba_bytes
    
    def create_temp_png_file(self, png_bytes):
        """Создает временный PNG файл"""
        try:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
            temp_file.write(png_bytes)
            temp_file.close()
            
            # Проверяем файл
            file_size = os.path.getsize(temp_file.name)
            logger.info(f"Created temp PNG file: {temp_file.name}, size: {file_size} bytes")
            
            return temp_file.name
        
        except Exception as e:
            logger.error(f"Error creating temp file: {str(e)}")
            return None
    
    def prepare_image_for_dalle2(self, image_source):
        """
        Подготавливает изображение для DALL-E 2 (требует RGBA PNG)

        Args:
            image_source: Путь к файлу или байты изображения

        Returns:
            str: Путь к временному PNG файлу в формате RGBA
        """
        try:
            # Загружаем изображение
            if isinstance(image_source, str) and os.path.exists(image_source):
                with open(image_source, 'rb') as f:
                    image_bytes = f.read()
                source_type = f"file: {image_source}"
            elif isinstance(image_source, bytes):
                image_bytes = image_source
                source_type = "bytes"
            else:
                logger.error(f"Invalid image source: {type(image_source)}")
                return None
            
            logger.info(f"Preparing image from {source_type}, size: {len(image_bytes)} bytes")
            
            # Конвертируем в RGBA PNG
            rgba_png_bytes = self.convert_to_rgba_png(image_bytes)
            if not rgba_png_bytes:
                logger.error("Failed to convert to RGBA PNG")
                return None
            
            # Делаем квадратным (рекомендовано для DALL-E 2)
            square_png_bytes = self.create_square_rgba_image(rgba_png_bytes, size=512)
            
            # Создаем временный файл
            temp_file_path = self.create_temp_png_file(square_png_bytes)
            
            return temp_file_path
        
        except Exception as e:
            logger.error(f"Error preparing image for DALL-E 2: {str(e)}")
            return None
    
    def generate_dalle2_variation(self, image_source, size="1024x1024"):
        """Генерирует вариацию через DALL-E 2"""
        try:
            # Подготавливаем изображение (RGBA PNG)
            temp_file_path = self.prepare_image_for_dalle2(image_source)
            if not temp_file_path:
                return {'success': False, 'error': 'Failed to prepare RGBA PNG image'}
            
            try:
                logger.info(f"Generating DALL-E 2 variation from {temp_file_path}")
                
                # Открываем файл и проверяем
                with Image.open(temp_file_path) as img:
                    logger.info(f"Image for variation: mode={img.mode}, size={img.size}, format={img.format}")
                
                # Отправляем в DALL-E 2
                with open(temp_file_path, 'rb') as image_file:
                    response = self.client.images.create_variation(
                        image=image_file,
                        model="dall-e-2",
                        n=1,
                        size=size,
                        response_format="url"
                    )
                
                image_url = response.data[0].url
                logger.info(f"DALL-E 2 variation successful, URL: {image_url}")
                
                result = self._download_and_encode_image(image_url)
                
                if result.get('success'):
                    result['operation'] = 'variation'
                    result['model'] = 'dall-e-2'
                
                return result
            
            finally:
                # Удаляем временный файл
                try:
                    if temp_file_path and os.path.exists(temp_file_path):
                        os.unlink(temp_file_path)
                        logger.info(f"Cleaned up temp file: {temp_file_path}")
                except:
                    pass
        
        except openai.OpenAIError as e:
            logger.error(f"DALL-E 2 variation error: {str(e)}")
            return {'success': False, 'error': f'DALL-E 2 error: {str(e)}'}
        except Exception as e:
            logger.error(f"Unexpected error in variation: {str(e)}", exc_info=True)
            return {'success': False, 'error': f'Unexpected error: {str(e)}'}
    
    def generate_dalle2_edit(self, base_image_source, mask_image_source, prompt, size="1024x1024"):
        """Редактирует изображение через DALL-E 2"""
        try:
            # Подготавливаем оба изображения
            base_temp_path = self.prepare_image_for_dalle2(base_image_source)
            mask_temp_path = self.prepare_image_for_dalle2(mask_image_source)
            
            if not base_temp_path or not mask_temp_path:
                return {'success': False, 'error': 'Failed to prepare RGBA PNG images'}
            
            try:
                logger.info(f"Generating DALL-E 2 edit with prompt: '{prompt[:50]}...'")
                
                # Проверяем изображения
                with Image.open(base_temp_path) as base_img, Image.open(mask_temp_path) as mask_img:
                    logger.info(f"Base image: mode={base_img.mode}, size={base_img.size}")
                    logger.info(f"Mask image: mode={mask_img.mode}, size={mask_img.size}")
                
                # Редактируем
                with open(base_temp_path, 'rb') as base_file, open(mask_temp_path, 'rb') as mask_file:
                    response = self.client.images.edit(
                        image=base_file,
                        mask=mask_file,
                        prompt=prompt,
                        model="dall-e-2",
                        n=1,
                        size=size,
                        response_format="url"
                    )
                
                image_url = response.data[0].url
                logger.info(f"DALL-E 2 edit successful, URL: {image_url}")
                
                result = self._download_and_encode_image(image_url, prompt)
                
                if result.get('success'):
                    result['operation'] = 'edit'
                    result['model'] = 'dall-e-2'
                
                return result
            
            finally:
                # Удаляем временные файлы
                for temp_path in [base_temp_path, mask_temp_path]:
                    try:
                        if temp_path and os.path.exists(temp_path):
                            os.unlink(temp_path)
                    except:
                        pass
        
        except openai.OpenAIError as e:
            logger.error(f"DALL-E 2 edit error: {str(e)}")
            return {'success': False, 'error': f'DALL-E 2 error: {str(e)}'}
        except Exception as e:
            logger.error(f"Unexpected error in edit: {str(e)}", exc_info=True)
            return {'success': False, 'error': f'Unexpected error: {str(e)}'}
    
    def generate_dalle3_image(self, prompt, size="1024x1024", quality="standard"):
        """Генерирует изображение через DALL-E 3"""
        try:
            logger.info(f"Generating DALL-E 3 image: '{prompt[:50]}...'")
            
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality=quality,
                n=1,
                response_format="url"
            )
            
            image_url = response.data[0].url
            logger.info(f"DALL-E 3 generation successful, URL: {image_url}")
            
            result = self._download_and_encode_image(image_url, prompt, model='dall-e-3')
            
            if result.get('success'):
                result['operation'] = 'generation'
                result['model'] = 'dall-e-3'
            
            return result
        
        except openai.OpenAIError as e:
            logger.error(f"DALL-E 3 error: {str(e)}")
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
                
                logger.info(f"Downloaded image: {len(image_data)} bytes, format: {img_format}")
                return result
            else:
                logger.error(f"Failed to download image: HTTP {img_response.status_code}")
                return {'success': False, 'error': f'Download failed: HTTP {img_response.status_code}'}
        
        except Exception as e:
            logger.error(f"Error downloading image: {str(e)}")
            return {'success': False, 'error': f'Download error: {str(e)}'}
    
    def process_image_generation(self, template_type, user_text=None, user_image_data=None, size=None):
        """Основная функция генерации"""
        try:
            # Получаем данные шаблона
            template_data = self.get_template_data(template_type)
            base_prompt = template_data.get('prompt', '')
            default_size = template_data.get('default_size', '1024x1024')
            final_size = size if size else default_size
            
            # Формируем промпт
            final_prompt = base_prompt
            if user_text and user_text.strip():
                final_prompt = f"{base_prompt}. Additional requirements: {user_text}"
            
            logger.info(f"Starting generation for '{template_type}', size: {final_size}")
            
            # Проверяем изображения
            base_image_path = template_data.get('image_path')
            has_template_image = base_image_path and os.path.exists(base_image_path)
            has_user_image = user_image_data is not None
            
            logger.info(f"Template image: {'exists' if has_template_image else 'not found'}")
            logger.info(f"User image: {'provided' if has_user_image else 'not provided'}")
            
            # Выбираем стратегию
            if has_template_image and has_user_image:
                logger.info("Strategy: Edit with mask")
                result = self.generate_dalle2_edit(
                    base_image_source=base_image_path,
                    mask_image_source=user_image_data,
                    prompt=final_prompt,
                    size=final_size
                )
            elif has_template_image:
                logger.info("Strategy: Variation from template")
                result = self.generate_dalle2_variation(
                    image_source=base_image_path,
                    size=final_size
                )
                if result.get('success'):
                    result['prompt'] = final_prompt
            elif has_user_image:
                logger.info("Strategy: Variation from user image")
                result = self.generate_dalle2_variation(
                    image_source=user_image_data,
                    size=final_size
                )
                if result.get('success'):
                    result['prompt'] = final_prompt
            else:
                logger.info("Strategy: Generate from scratch")
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
                logger.info(f"Successfully generated image")
            
            return result
        
        except Exception as e:
            logger.error(f"Error in generation process: {str(e)}", exc_info=True)
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
    # Размеры для разных типов
    size_mapping = {
        'business': "1024x1024",
        'greeting': "1024x1024",
        'congratulation': "1024x1024",
        'birthday': "1024x1024",
        'postcard': "1024x1792",
        'landscape': "1792x1024",
        'instagram': "1080x1080",
        'story': "1080x1920",
        'square': "1024x1024",
        'portrait': "1024x1792",
        'wide': "1792x1024",
    }
    
    size = size_mapping.get(template_type.lower(), "1024x1024")
    
    logger.info(f"process_with_gpt called: template={template_type}")
    
    return image_generator.process_image_generation(
        template_type=template_type,
        user_text=text,
        user_image_data=image_data,
        size=size
    )