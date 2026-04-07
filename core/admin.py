from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Carousel, GeneralData, Support, Country, State, City, Thana, Testimonial
from django.core.exceptions import ValidationError

@admin.register(Carousel)
class CarouselAdmin(ModelAdmin):
    list_display = ['title', 'title_bn', 'subtitle', 'subtitle_bn', 'image', 'link', 'index_number', 'is_active']
    list_editable = ['index_number', 'is_active']
    search_fields = ['title', 'title_bn', 'subtitle', 'subtitle_bn']
    list_per_page = 10

    def save_model(self, request, obj, form, change):
        if not obj.index_number:
            obj.index_number = Carousel.objects.count() + 1
        super().save_model(request, obj, form, change)


@admin.register(GeneralData)
class GeneralDataAdmin(ModelAdmin):
    list_display = ['address', "address_bn", 'phone', 'delivery_charge']
    fieldsets = (
        ("Contact Information", {
            'fields': ('address', 'address_bn',  'phone', 'email', 'facebook', 'twitter', 'instagram', 'youtube', 'linkedin')
        }),
        ('Home Page Articles Section', {
            'fields': ('articles_section_title', 'articles_section_title_bn', 'articles_section_subtitle', 'articles_section_subtitle_bn')
        }),
        ('Delivery Charge', {
            'fields': ('delivery_charge',)
        }),
        ('Website Logo', {
            'fields': ('website_logo',)
        }),
    )



@admin.register(Support)
class SupportAdmin(ModelAdmin):
    list_display = ['name', 'email', 'phone', 'message']
    list_per_page = 10

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Country)
class CountryAdmin(ModelAdmin):
    list_display = ['name', 'name_bn', 'code', 'flag']
    list_per_page = 10


@admin.register(State)
class StateAdmin(ModelAdmin):
    list_display = ['name', 'name_bn', 'country']
    list_per_page = 10


@admin.register(City)
class CityAdmin(ModelAdmin):
    list_display = ['name', 'name_bn', 'state']
    list_per_page = 10


@admin.register(Thana)
class ThanaAdmin(ModelAdmin):
    list_display = ['name', 'name_bn', 'city'] 
    list_per_page = 10


@admin.register(Testimonial)
class TestimonialAdmin(ModelAdmin):
    list_display = ['name', 'name_bn', 'designation', 'designation_bn', 'city', 'city_bn', 'rating', 'is_active']
    list_per_page = 20
    list_filter = ['is_active']
    search_fields = ['name', 'designation', 'city']
    list_editable = ['is_active']

