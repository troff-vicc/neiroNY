from django.contrib import admin
from django.utils.html import format_html
from .models import CardTemplate


@admin.register(CardTemplate)
class CardTemplateAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'is_active',
        'created_at',
        'updated_at'
    ]
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'prompt']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'prompt', 'is_active')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def log_addition(self, *args, **kwargs):
        """Отключаем логирование добавления"""
        return None
    
    def log_change(self, *args, **kwargs):
        """Отключаем логирование изменения"""
        return None
    
    def log_deletion(self, *args, **kwargs):
        """Отключаем логирование удаления"""
        return None
        