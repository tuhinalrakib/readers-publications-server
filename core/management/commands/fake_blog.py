from django.core.management.base import BaseCommand
from faker import Faker
import random
from blog.models import Blog
from django.utils import timezone
from django.core.files.base import ContentFile
import requests

fake = Faker()

class Command(BaseCommand):
    help = 'Seed the database with fake blog posts'

    def handle(self, *args, **kwargs):
        for _ in range(50):
            # Optional: download a random image as cover
            image_url = "https://picsum.photos/600/400"
            image_response = requests.get(image_url)
            image_name = f"{fake.uuid4()}.jpg"
            image_file = ContentFile(image_response.content, name=image_name)

            blog = Blog.objects.create(
                author_name=fake.name(),
                author_name_bn=fake.name(),
                title=fake.sentence(nb_words=6),
                title_bn=fake.sentence(nb_words=6),
                subtitle=fake.sentence(nb_words=10),
                subtitle_bn=fake.sentence(nb_words=10),
                content=fake.paragraph(nb_sentences=10),
                content_bn=fake.paragraph(nb_sentences=10),
                cover_image=image_file,
                author_image=image_file,
                read_time=random.randint(1, 10),
                is_active=random.choice([True, False]),
                published_date=fake.date_time_between(start_date='-1y', end_date='now', tzinfo=timezone.get_current_timezone()),
            )
            self.stdout.write(self.style.SUCCESS(f'Created Blog: {blog.title}'))
