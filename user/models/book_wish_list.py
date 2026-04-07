from django.db import models
from .user import User
from book.models import Book
from core.models import BaseModel
from django.core.exceptions import ValidationError


class BookWishList(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='wishlist')

    def __str__(self):
        return f"{self.user.email} - {self.book.title}"

    class Meta:
        verbose_name = "Book Wish List"
        verbose_name_plural = "Book Wish Lists"
        
    def clean(self):
        if BookWishList.objects.filter(user=self.user, book=self.book).exists():
            raise ValidationError("Book already in wishlist")
