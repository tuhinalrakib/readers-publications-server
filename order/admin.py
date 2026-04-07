from django.contrib import admin
from order.models import Order, OrderItem
from unfold.admin import ModelAdmin


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = (
        'order_id', 'user', 'sub_total', 'shipping_cost', 'total_amount', 'status', 'shipping_address', 'payment'
    )
    list_editable = ('status',)
    search_fields = ('order_id', 'user', 'sub_total', 'shipping_cost', 'total_amount', 'status')
    ordering = ('order_id',)

@admin.register(OrderItem)
class OrderItemAdmin(ModelAdmin):
    list_display = ('order', 'book', 'quantity', 'price')
    search_fields = ('order', 'book', 'quantity', 'price')
    ordering = ('order',)
