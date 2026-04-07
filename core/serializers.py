from rest_framework import serializers
from .models import Support, GeneralData, Carousel, Testimonial
from django.conf import settings

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
        return f"{settings.BACKEND_SITE_HOST}{obj.image.url}" if obj.image else ""


class TestimonialSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Testimonial
        fields = ['name', 'name_bn', 'designation', 'designation_bn', 'city', 'city_bn', 'comment', 'comment_bn', 'rating', 'image_url']

    def get_image_url(self, obj):
        return f"{settings.BACKEND_SITE_HOST}{obj.image.url}" if obj.image else ""