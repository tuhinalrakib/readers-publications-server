from cart.models import Cart
from cart.serializers import CartSerializerRead, CartSerializerCreate
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

class CartView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Cart.objects.filter()
    serializer_class = CartSerializerRead
    lookup_field = 'uuid'

    def get_queryset(self):
        if self.request.query_params.get('is_selected'):
            return Cart.objects.filter(user=self.request.user, is_selected=True)
        return Cart.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return CartSerializerCreate
        return CartSerializerRead

    @action(detail=True, methods=['patch'])
    def update_quantity(self, request, uuid=None):
        cart = get_object_or_404(Cart, uuid=uuid)

        quantity = request.data.get('quantity')
        if quantity is not None:
            try:
                quantity = int(quantity)
                if quantity < 1:
                    return Response({'error': 'Quantity must be at least 1'}, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({'error': 'Quantity must be an integer'}, status=status.HTTP_400_BAD_REQUEST)

            cart.quantity = quantity
            cart.save()
            return Response(CartSerializerRead(cart).data, status=status.HTTP_200_OK)

        return Response({'error': 'Quantity is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def update_checkout_selection_status(self, request):
        try:
            cart_ids = request.data.get('cart_ids')
            is_selected = request.data.get('is_selected')
            carts = []
            for cart_id in cart_ids:
                cart = get_object_or_404(Cart, uuid=cart_id)
                cart.is_selected = is_selected
                carts.append(cart)
            Cart.objects.bulk_update(carts, ['is_selected'])
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
