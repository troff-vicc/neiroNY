from rest_framework import serializers
from ..models import CardTemplate


class CardTemplateSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = CardTemplate
        fields = [
            'id',
            'title',
            'prompt',
            'image',
            'image_url',
            'created_at',
            'updated_at',
            'is_active'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_image_url(self, obj):
        """Возвращает полный URL изображения"""
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class CardTemplateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardTemplate
        fields = ['title', 'prompt', 'image', 'is_active']