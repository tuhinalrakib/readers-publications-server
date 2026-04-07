from django.contrib import admin
from cart.models import Cart
from unfold.admin import ModelAdmin


@admin.register(Cart)
class CartAdmin(ModelAdmin):
    list_display = ['uuid', 'user', 'book', 'quantity', 'is_selected']
    list_filter = ['is_selected']
    search_fields = ['user__username', 'book__title', 'uuid']
    list_per_page = 10

