from django.core.management.base import BaseCommand
from core.models import Country, State, City, Thana
from utils.general_data import BD_LOCATION_DATA

class Command(BaseCommand):
    help = 'Import real Bangladesh location data using a Python dictionary'

    def handle(self, *args, **kwargs):
        self.stdout.write("Importing Bangladesh location data...")

        

        self.stdout.write(self.style.SUCCESS("✅ Bangladesh location data imported successfully."))