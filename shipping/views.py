from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .models import Shipping
from .serializers import ShippingCreateSerializer, ShippingReadSerializer
from rest_framework.permissions import IsAuthenticated

class ShippingModelViewSet(ModelViewSet):
    queryset = Shipping.objects.all()
    serializer_class = ShippingReadSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return ShippingCreateSerializer
        return ShippingReadSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user, is_active=True)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Access the saved instance
        instance = serializer.instance

        # Use read serializer for response
        read_data = ShippingReadSerializer(instance).data
        headers = self.get_success_headers(serializer.data)
        return Response(read_data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        instance = self.get_object()
        data = ShippingReadSerializer(instance).data
        return Response(data, status=response.status_code)

