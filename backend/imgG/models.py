from django.db import models
from django.utils.text import slugify
import os


class CardTemplate(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Название шаблона"
    )
    prompt = models.TextField(
        verbose_name="Заготовленный промт",
        help_text="Промт для генерации контента открытки"
    )
    image = models.ImageField(
        upload_to='card_templates/',  # ПРОСТО ПУТЬ БЕЗ ФУНКЦИИ
        verbose_name="Изображение шаблона",
        help_text="Загрузите изображение шаблона"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активный"
    )

    def __str__(self):
        return self.title

    