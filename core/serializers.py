from rest_framework import serializers
from .models import Support, GeneralData, Carousel, Testimonial
from core.utils import build_media_url

class SupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Support
        fields = ['name', 'email', 'phone', 'message']


class CarouselSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Carousel
        fields = ['title', 'title_bn', 'subtitle', 'subtitle_bn', 'image_url', 'link']

    def get_image_url(self, obj):
        return build_media_url(obj.image) or ""


class TestimonialSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Testimonial
        fields = ['name', 'name_bn', 'designation', 'designation_bn', 'city', 'city_bn', 'comment', 'comment_bn', 'rating', 'image_url']

    def get_image_url(self, obj):
        return build_media_url(obj.image) or ""
