from django.core.management.base import BaseCommand
from core.models import Country, State, City, Thana
from utils.general_data import BD_LOCATION_DATA

class Command(BaseCommand):
    help = 'Import real Bangladesh location data using a Python dictionary'

    def handle(self, *args, **kwargs):
        self.stdout.write("Importing Bangladesh location data...")

        country, _ = Country.objects.get_or_create(name='Bangladesh', name_bn="বাংলাদেশ")
        divisions = BD_LOCATION_DATA.get("divisions")
        
        for division in divisions:
            division_name = division.get("name")
            division_name_bn = division.get("name_bn")
            state, created = State.objects.get_or_create(name=division_name, name_bn=division_name_bn, country=country)
            for district in division.get("districts"):
                district_name = district.get("name")
                district_name_bn = district.get("name_bn")
                city, created = City.objects.get_or_create(name=district_name, name_bn=district_name_bn, state=state)
                for thana in district.get("thanas"):
                    thana_name = thana.get("name")
                    thana_name_bn = thana.get("name_bn")
                    Thana.objects.get_or_create(name=thana_name, name_bn=thana_name_bn, city=city)
                 
        self.stdout.write(self.style.SUCCESS("✅ Bangladesh location data imported successfully."))
