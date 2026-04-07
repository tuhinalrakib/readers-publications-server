import random
from django.core.management.base import BaseCommand
from book.models import BookReview
from faker import Faker
from django.contrib.auth import get_user_model
from book.models import Book
from django.db.models import Avg
from django.db.models.functions import Round
from django.db.models import Count
from django.db.models import F


class Command(BaseCommand):
    help = 'Generate fake book reviews'
    
    def handle(self, *args, **kwargs):
        fake = Faker()
        users = get_user_model().objects.all()
        books = Book.objects.all()

        for book in books:
            for i in range(random.randint(1, 50)):
                if BookReview.objects.filter(book=book, user=random.choice(users)).exists():
                    continue
                
                BookReview.objects.create(
                    book=book,
                    user=random.choice(users),
                    review=fake.sentence(),
                    rating=random.randint(1, 5)
                )

        self.stdout.write(self.style.SUCCESS(f'Successfully generated {BookReview.objects.count()} fake book reviews'))



