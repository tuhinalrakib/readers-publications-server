from django.db import models
from django.utils import timezone
from django.utils.timezone import timedelta
from .user import User
from core.models import BaseModel

class VerificationCode(BaseModel):
    TYPE_EMAIL = 'email'
    TYPE_PHONE = 'phone'
    TYPE_2FA = '2fa'

    VERIFICATION_TYPE_CHOICES = [
        (TYPE_EMAIL, 'Email'),
        (TYPE_PHONE, 'Phone'),
        (TYPE_2FA, 'Two-Factor'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=VERIFICATION_TYPE_CHOICES)
    is_used = models.BooleanField(default=False)

    def is_expired(self):
        expiry_map = {
            self.TYPE_EMAIL: timedelta(hours=24),
            self.TYPE_PHONE: timedelta(minutes=30),
            self.TYPE_2FA: timedelta(minutes=5),
        }
        return timezone.now() > self.created_at + expiry_map[self.type]
    
    def verify_code(self, code_input):
        if self.is_expired():
            return False
        if self.is_used:
            return False
        if self.code == code_input:
            self.is_used = True
            self.save()
            return True
        return False
