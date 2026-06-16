from rest_framework import serializers
from book.models import Category
from core.utils import build_media_url

class CategorySerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "name_bn", "description", "image_url", "slug", "index_number", "is_featured"]

    def get_image_url(self, obj):
        return build_media_url(obj.image) or ""
 
