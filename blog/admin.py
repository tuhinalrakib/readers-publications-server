from django.contrib import admin
from .models import Blog
from django_ckeditor_5.fields import CKEditor5Field
from django_ckeditor_5.widgets import CKEditor5Widget
from unfold.admin import ModelAdmin


@admin.register(Blog)
class BlogAdmin(ModelAdmin):
    list_display = ['title', 'author_name', 'published_date', 'is_active', 'is_featured', 'index_number']
    list_editable = ['is_active', 'is_featured', 'index_number']
    list_filter = ['is_active']
    search_fields = ['title', 'title_bn', 'subtitle', 'subtitle_bn', 'author_name', 'author_name_bn']
    list_per_page = 10
    formfield_overrides = {
        CKEditor5Field: {'widget': CKEditor5Widget},
    }