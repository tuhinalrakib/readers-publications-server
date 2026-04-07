from django.core.management.base import BaseCommand
from faker import Faker
import random
import requests
from core.models import Testimonial  # Change this if your model is in a different app
from django.core.files.base import ContentFile

fake = Faker()
Faker.seed(0)

class Command(BaseCommand):
    help = 'Seed the database with fake testimonials'

    def handle(self, *args, **kwargs):
        for _ in range(50):
            # Optional: random profile image
            image_url = 'https://i.pravatar.cc/150?img=' + str(random.randint(1, 70))
            response = requests.get(image_url)
            image_name = f"testimonial_{fake.uuid4()}.jpg"
            image_file = ContentFile(response.content, name=image_name)

            testimonial = Testimonial.objects.create(
                name=fake.name(),
                name_bn=fake.name(),
                designation=fake.job(),
                designation_bn=fake.job(),
                city=fake.city(),
                city_bn=fake.city(),
                comment=fake.paragraph(nb_sentences=5),
                comment_bn=fake.paragraph(nb_sentences=5),
                image=image_file,
                rating=random.randint(1, 5),
                is_active=random.choice([True, False])
            )
            self.stdout.write(self.style.SUCCESS(f'Created testimonial from: {testimonial.name}'))
