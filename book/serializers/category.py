from rest_framework import serializers
from book.models import Category
from django.conf import settings

class CategorySerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "name_bn", "description", "image_url", "slug", "index_number", "is_featured"]

    def get_image_url(self, obj):
        return f"{settings.BACKEND_SITE_HOST}{obj.image.url}" if obj.image else ""
 