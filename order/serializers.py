from cart.models import Cart
from payment.models import Payment
from rest_framework import serializers
from .models import Order, OrderStatus
from .models import OrderItem
from shipping.models import Shipping
from core.models import GeneralData
from django.utils import timezone
from django.conf import settings


class OrderCreateSerializer(serializers.ModelSerializer):
    shipping_address_id = serializers.CharField(required=True, allow_null=False, write_only=True)
    payment_method = serializers.CharField(required=True, allow_null=False, write_only=True)
    mobile_number = serializers.CharField(allow_null=True, required=False, allow_blank=True, write_only=True)
    reference_number = serializers.CharField(allow_null=True, required=False, allow_blank=True, write_only=True)
    
    class Meta:
        model = Order
        fields = ['order_id', 'shipping_address_id', 'payment_method', 'mobile_number', 'reference_number']
        read_only_fields = ['order_id']
        
    def validate(self, attrs):
        payment_method = attrs.get('payment_method')
        if payment_method not in ['bkash', 'nagad', 'rocket', 'cod']:
            raise serializers.ValidationError("Invalid payment method")
        
        if payment_method in ['bkash', 'nagad', 'rocket']:
            if not attrs.get('mobile_number') or not attrs.get('reference_number'):
                raise serializers.ValidationError("Mobile number and reference number are required for mobile payment")
            
        shipping_address_id = attrs.get('shipping_address_id')
        shipping_address = Shipping.objects.filter(id=shipping_address_id, user=self.context['request'].user).first()
        if not shipping_address:
            raise serializers.ValidationError("Your shipping address is not valid")
        
        # get cart items
        cart_items = Cart.objects.filter(user=self.context['request'].user, is_selected=True)
        if not cart_items.exists():
            raise serializers.ValidationError("No cart items found")
        
        attrs['shipping_address'] = shipping_address
        del attrs['shipping_address_id']
                
        return attrs
    
    def create(self, validated_data):
        payment_method = validated_data.pop('payment_method')
        mobile_number = validated_data.pop('mobile_number')
        reference_number = validated_data.pop('reference_number')
        
        # get cart items
        cart_items = Cart.objects.filter(user=self.context['request'].user, is_selected=True)
        # get total price
        sub_total = sum(item.book.get_book_price() * item.quantity for item in cart_items)
        general_data = GeneralData.objects.first()
        if general_data.delivery_charge:
            shipping_cost = general_data.delivery_charge
        else:
            shipping_cost = 0
        total_amount = sub_total + shipping_cost
        
        # create order
        order = Order.objects.create(
            user=self.context['request'].user,
            sub_total=sub_total,
            shipping_cost=shipping_cost,
            total_amount=total_amount,
            status=OrderStatus.PENDING,
            shipping_address=validated_data['shipping_address'],
        )
        
        # create order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.book.get_book_price() * item.quantity,
            )
            
        # delete cart items
        cart_items.delete()
        
        # create payment
        payment = Payment.objects.create_payment(
            user=self.context['request'].user,
            amount=total_amount,
            payment_method=payment_method,
            payment_date=timezone.now(),
            mobile_number=mobile_number,
            reference_number=reference_number,
        )
        
        # update order with payment
        order.payment = payment
        order.save()
        return order


class OrderItemSerializer(serializers.ModelSerializer):
    book = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = ['id', 'book', 'quantity', 'price']
    
    def get_book(self, obj):
        book = obj.book
        return {
            "slug": book.slug,
            "title": book.title,
            "price": book.get_book_price(),
            "cover_image": settings.BACKEND_SITE_HOST + book.cover_image.url if book.cover_image else None,
            "has_review": book.reviews.filter(is_active=True, user=self.context['request'].user).exists(),
        }


class OrderListSerializer(serializers.ModelSerializer):
    order_items_count = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%d %B %Y")
    
    class Meta:
        model = Order
        fields = ['id', 'order_id', "status", "created_at", "total_amount", "order_items_count"]

    def get_order_items_count(self, obj):
        order_items = OrderItem.objects.filter(order=obj).count()
        return order_items


class OrderDetailSerializer(serializers.ModelSerializer):
    payment_details = serializers.SerializerMethodField()
    order_items = serializers.SerializerMethodField()
    shipping_address = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ['id', 'order_id', "status", "sub_total", "shipping_cost", "payment_details", "order_items", "shipping_address"]

    def get_payment_details(self, obj):
        payment = obj.payment
        if payment:
            return {
                "id": payment.id,
                "payment_method": payment.payment_method,
                "payment_status": payment.payment_status,
                "payment_date": payment.payment_date.strftime("%d %B %Y, %H:%M %p") if payment.payment_date else None,
                "mobile_number": payment.get_payment_method_obj().mobile_number if payment.get_payment_method_obj() else None,
                "reference_number": payment.get_payment_method_obj().reference_number if payment.get_payment_method_obj() else None,
            }
        return None
    
    def get_shipping_address(self, obj):
        shipping_address = obj.shipping_address
        if shipping_address:
            return {
                "id": shipping_address.id,
                "address_type": shipping_address.address_type,
                "name": shipping_address.name,
                "phone": shipping_address.phone,
                "email": shipping_address.email,
                "state_name": shipping_address.state.name if shipping_address.state else None,
                "state_name_bn": shipping_address.state.name_bn if shipping_address.state else None,
                "city_name": shipping_address.city.name if shipping_address.city else None,
                "city_name_bn": shipping_address.city.name_bn if shipping_address.city else None,
                "thana_name": shipping_address.thana.name if shipping_address.thana else None,
                "thana_name_bn": shipping_address.thana.name_bn if shipping_address.thana else None,
                "detail_address": shipping_address.detail_address,
                "note": shipping_address.note,
                "courier_service_name": shipping_address.courier_service_name if shipping_address.courier_service_name else None,
                "courier_service_tracking_id": shipping_address.courier_service_tracking_id if shipping_address.courier_service_tracking_id else None,
            }
        return None
    
    def get_order_items(self, obj):
        order_items = OrderItem.objects.filter(order=obj)
        return OrderItemSerializer(order_items, many=True, context=self.context).data
  