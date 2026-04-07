from rest_framework import serializers
from .models import Blog
from django.conf import settings

class BlogSerializerListRead(serializers.ModelSerializer):
    cover_image = serializers.SerializerMethodField()
    published_date = serializers.SerializerMethodField()

    def get_cover_image(self, obj):
        return f"{settings.BACKEND_SITE_HOST}{obj.cover_image.url}" if obj.cover_image else None
    
    def get_published_date(self, obj):
        return obj.published_date.strftime("%B %d, %Y") if obj.published_date else None
    
    class Meta:
        model = Blog
        fields = [
            'id',
            'slug',
            'title',
            'title_bn',
            'subtitle',
            'subtitle_bn',
            'cover_image',
            'read_time',
            'author_name',
            'author_name_bn',
            'cover_image',
            'published_date'
        ]

from django.conf import settings
import re
from rest_framework import serializers
from .models import Blog

class BlogSerializerDetailRead(serializers.ModelSerializer):
    cover_image = serializers.SerializerMethodField()
    published_date = serializers.SerializerMethodField()
    author_image = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    content_bn = serializers.SerializerMethodField()

    def get_cover_image(self, obj):
        return f"{settings.BACKEND_SITE_HOST}{obj.cover_image.url}" if obj.cover_image else None
    
    def get_published_date(self, obj):
        return obj.published_date.strftime("%B %d, %Y") if obj.published_date else None
    
    def get_author_image(self, obj):
        return f"{settings.BACKEND_SITE_HOST}{obj.author_image.url}" if obj.author_image else None
    
    def get_content(self, obj):
        if obj.content:
            # Replace relative media URLs with full backend host URL
            return re.sub(
                r'src="/media/([^"]+)"',
                f'src="{settings.BACKEND_SITE_HOST}/media/\\1"',
                obj.content
            )
        return None
    
    def get_content_bn(self, obj):
        if obj.content_bn:
            # Replace relative media URLs with full backend host URL
            return re.sub(
                r'src="/media/([^"]+)"',
                f'src="{settings.BACKEND_SITE_HOST}/media/\\1"',
                obj.content_bn
            )
        return None

    class Meta:
        model = Blog
        fields = [
            'id',
            'slug',
            'title',
            'title_bn',
            'subtitle',
            'subtitle_bn',
            'content',
            'content_bn',
            'cover_image',
            'read_time',
            'author_name',
            'author_name_bn',
            'published_date',
            'author_image'
        ]
