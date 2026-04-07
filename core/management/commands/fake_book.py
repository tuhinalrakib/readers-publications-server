import random
from decimal import Decimal
from faker import Faker
from django.core.management.base import BaseCommand
from book.models import Book, Category, Tag  # adjust if your app is not 'books'
from user.models import User
from django.utils.text import slugify
from author.models import Author

class Command(BaseCommand):
    help = 'Generate 50 fake book entries'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Get an author
        user = User.objects.first()
        author = Author.objects.first()
        if not author:
            Author.objects.create(user=user)
            return

        # Get or create categories and tags
        categories = list(Category.objects.all()[:5])
        if not categories:
            for _ in range(5):
                categories.append(Category.objects.create(name=fake.word()))

        tags = list(Tag.objects.all()[:5])
        if not tags:
            for _ in range(5):
                tags.append(Tag.objects.create(name=fake.word()))

        for _ in range(50):
            title = fake.sentence(nb_words=5)
            book = Book.objects.create(
                title=title,
                title_bn=fake.sentence(nb_words=3),
                slug=slugify(title),
                author=author,
                status=random.choice(['published', 'draft', 'archived']),
                sku=fake.unique.bothify(text='SKU-#####'),
                description=fake.paragraph(nb_sentences=3),
                published_date=fake.date_between(start_date='-5y', end_date='today'),
                isbn=fake.isbn13(separator=""),
                pages=random.randint(50, 1000),
                is_available=random.choice([True, False]),
                price=Decimal(random.uniform(100.0, 1000.0)).quantize(Decimal('0.01')),
                discounted_price=Decimal(random.uniform(50.0, 900.0)).quantize(Decimal('0.01')),
                available_copies=random.randint(0, 100),
                rating=Decimal(random.uniform(0.0, 5.0)).quantize(Decimal('0.01')),
                rating_count=random.randint(0, 1000),
                publisher_name=fake.company(),
                translator=fake.name() if random.choice([True, False]) else "",
                edition=f"{random.randint(1, 5)}th",
                language=random.choice(['English', 'Bengali', 'Hindi', 'Spanish']),
                dimensions="5 x 8 inches",
                weight=Decimal(random.uniform(100, 1000)).quantize(Decimal('0.01')),
                country=fake.country(),
                is_new_arrival=random.choice([True, False]),
                is_popular=random.choice([True, False]),
                is_comming_soon=random.choice([True, False]),
                is_best_seller=random.choice([True, False]),
                is_active=True,
            )
            book.categories.set(random.sample(categories, random.randint(1, len(categories))))
            book.tags.set(random.sample(tags, random.randint(1, len(tags))))

        self.stdout.write(self.style.SUCCESS('✅ Successfully created 50 fake books.'))
