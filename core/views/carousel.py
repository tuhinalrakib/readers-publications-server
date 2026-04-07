from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from core.models import Carousel
from core.serializers import CarouselSerializer

class CarouselListViewSet(viewsets.ViewSet):
    def list(self, request):
        carousel_items = Carousel.objects.filter(is_active=True).order_by('index_number')
        serializer = CarouselSerializer(carousel_items, many=True, context={'request': request})
        carousel_items = serializer.data
        return Response(carousel_items, status=status.HTTP_200_OK)
