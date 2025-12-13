from django.contrib import admin
from django.utils.html import format_html
from .models import CardTemplate


@admin.register(CardTemplate)
class CardTemplateAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'display_image',
        'is_active',
        'created_at',
        'updated_at'
    ]
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'prompt']
    readonly_fields = ['created_at', 'updated_at', 'display_image_large']
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'prompt', 'is_active')
        }),
        ('Изображение', {
            'fields': ('image', 'display_image_large')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def display_image(self, obj):
        """Отображение миниатюры в списке"""
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover;" />',
                obj.image.url
            )
        return "Нет изображения"
    
    display_image.short_description = "Миниатюра"
    
    def display_image_large(self, obj):
        """Отображение большого изображения в форме редактирования"""
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px;" />',
                obj.image.url
            )
        return "Нет изображения"
    
    display_image_large.short_description = "Предпросмотр изображения"
    
    def save_model(self, request, obj, form, change):
        """Переопределяем сохранение для отладки"""
        try:
            
            # Сохраняем сначала без файла
            if 'image' in form.files:
                file = form.files['image']
                print(f"DEBUG: Файл получен: {file.name}, размер: {file.size}")
            
            # Пробуем сохранить
            super().save_model(request, obj, form, change)
        
        except Exception as e:
            print(f"DEBUG: Ошибка при сохранении: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            raise  # Пробрасываем дальше
    
    def log_addition(self, *args, **kwargs):
        """Отключаем логирование добавления"""
        return None
    
    def log_change(self, *args, **kwargs):
        """Отключаем логирование изменения"""
        return None
    
    def log_deletion(self, *args, **kwargs):
        """Отключаем логирование удаления"""
        return None
        