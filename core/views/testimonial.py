from rest_framework.generics import ListAPIView
from core.models import Testimonial
from core.serializers import TestimonialSerializer

class TestimonialListAPIView(ListAPIView):
    queryset = Testimonial.objects.filter(is_active=True)
    serializer_class = TestimonialSerializer

    def get_queryset(self):
        return Testimonial.objects.filter(is_active=True).order_by('-created_at')