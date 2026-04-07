import random
from django.db import models

from core.models import BaseModel
from user.models import User
from shipping.models import Shipping
from payment.models import Payment


class OrderStatus(models.TextChoices):
    PENDING = 'pending'
    PROCESSING = 'processing'
    READY_TO_SHIP = 'ready_to_ship'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'


class Order(BaseModel):
    order_id = models.CharField(max_length=255, unique=True) # tracking id
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default='pending')
    shipping_address = models.ForeignKey(Shipping, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.total_amount}"
    
    def save(self, *args, **kwargs):
        if not self.order_id:
            while Order.objects.filter(order_id=self.order_id).exists():
                self.order_id = f"{random.randint(1000000, 9999999)}"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ['-created_at']


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey("book.Book", on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.order.order_id} - {self.book.title}"

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
        ordering = ['-created_at']
