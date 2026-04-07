from django.contrib import admin

from .models import Author, AuthorTag
from unfold.admin import ModelAdmin

class AuthorTagTabularInline(admin.TabularInline):
    model = AuthorTag
    extra = 1
    fields = ('name', 'name_bn')
    autocomplete_fields = ('author',)

@admin.register(Author)
class AuthorAdmin(ModelAdmin):
    inlines = [AuthorTagTabularInline]
    list_display = ('name', 'name_bn', 'email', 'phone_number', 'city', 'state', 'country', 'is_active')
    list_filter = ('city', 'state', 'country')
    search_fields = ('name', 'name_bn', 'email', 'phone_number', 'city', 'state', 'country')
    list_editable = ('is_active',)
    
