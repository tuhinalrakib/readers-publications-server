from django.db import models
import uuid
from core.models import BaseModel
from book.models import Book
from user.models import User

class Cart(BaseModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='cart')
    quantity = models.PositiveIntegerField(default=1)
    is_selected = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"
        ordering = ['-created_at']

