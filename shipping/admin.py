from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Shipping

@admin.register(Shipping)
class ShippingAdmin(ModelAdmin):
    list_display = ['user', 'address_type', 'name', 'phone', 'email', 'state', 'city', 'thana', 'is_default', 'is_active']
    list_filter = ['state', 'city', 'thana', 'is_default', 'is_active']
    search_fields = ['name', 'phone', 'email', 'detail_address']
    list_per_page = 10
