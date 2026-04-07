import random
import string
from django.db import models

from core.models import BaseModel
from user.models import User


class PaymentMethod(models.TextChoices):
    CASH_ON_DELIVERY = 'cod'
    BANK_TRANSFER = 'bank_transfer'
    BKASH = 'bkash'
    ROCKET = 'rocket'
    NAGAD = 'nagad'


class PaymentStatus(models.TextChoices):
    PENDING = 'pending'
    PAID = 'paid'
    FAILED = 'failed'
    

class PaymentModelManager(models.Manager):
    def create_payment(self, user, amount, payment_method, payment_date, mobile_number=None, reference_number=None):
        payment = self.create(
            user=user,
            amount=amount,
            payment_method=payment_method,
            payment_date=payment_date,
        )
        if payment_method == PaymentMethod.BKASH:
            BkashPayment.objects.create(
                payment=payment,
                mobile_number=mobile_number,
                reference_number=reference_number,
            )
        elif payment_method == PaymentMethod.ROCKET:
            RocketPayment.objects.create(
                payment=payment,
                mobile_number=mobile_number,
                reference_number=reference_number,
            )
        elif payment_method == PaymentMethod.NAGAD:
            NagadPayment.objects.create(
                payment=payment,
                mobile_number=mobile_number,
                reference_number=reference_number,
            )
            
        return payment


class Payment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices, default='cash_on_delivery')
    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices, default='pending')
    payment_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    payment_id = models.CharField(max_length=255, blank=True, null=True)

    objects = PaymentModelManager()
    
    def __str__(self):
        return f"{self.payment_id}"
    
    def save(self, *args, **kwargs):
        if not self.payment_id:
            while Payment.objects.filter(payment_id=self.payment_id).exists():
                self.payment_id = f"{random.randint(1000000, 9999999)}"
        super().save(*args, **kwargs)
        
    def get_payment_method_obj(self):
        if self.payment_method == PaymentMethod.BKASH:
            return self.bkash_payments.first()
        elif self.payment_method == PaymentMethod.ROCKET:
            return self.rocket_payments.first()
        elif self.payment_method == PaymentMethod.NAGAD:
            return self.nagad_payments.first()
        return None

class BkashPayment(BaseModel):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='bkash_payments')
    mobile_number = models.CharField(max_length=255)
    reference_number = models.CharField(max_length=255)


class NagadPayment(BaseModel):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='nagad_payments')
    mobile_number = models.CharField(max_length=255)
    reference_number = models.CharField(max_length=255)


class RocketPayment(BaseModel):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='rocket_payments')
    mobile_number = models.CharField(max_length=255)
    reference_number = models.CharField(max_length=255)
