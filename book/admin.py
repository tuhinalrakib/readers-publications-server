from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Book, Category, SpecialPackage, SpecialPackageBook, BookImage, BookPreview, BookReview
from django import forms
from django.forms.widgets import Select, Input
from django import forms

class BookImageInline(admin.TabularInline):
    model = BookImage
    extra = 1
    autocomplete_fields = ['book']
    show_change_link = True
    classes = ['tab', 'shadow-md', 'rounded-xl', 'p-4', 'bg-gray-500']
    fields = ["image", "alt_text", "index_number", "is_active"]

class BookPreviewInline(admin.TabularInline):
    model = BookPreview
    extra = 1
    autocomplete_fields = ['book']
    show_change_link = True
    classes = ['tab', 'shadow-md', 'rounded-xl', 'p-4', 'bg-gray-500']
    fields = ["image", "index_number", "is_active"]


@admin.register(Book)
class BookAdmin(ModelAdmin):
    list_display = (
        'title', 'title_bn', 'status', 'is_available', 'is_new_arrival', 'is_popular', 'is_comming_soon', 'is_best_seller', 'is_active',
        'sku', 'isbn', 'price', 'discounted_price', 'available_copies'
    )
    list_filter = ('status', 'is_available', 'is_new_arrival', 'is_popular', 'is_comming_soon', 'is_best_seller', 'is_active')
    list_editable = ('status', 'is_available', 'is_new_arrival', 'is_popular', 'is_comming_soon', 'is_best_seller', 'is_active')
    list_per_page = 10
    list_max_show_all = 100
    search_fields = ('title', 'title_bn', 'sku', 'isbn', 'publisher_name', 'translator', 'edition', 'language', 'dimensions', 'weight', 'country')
    ordering = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [BookImageInline, BookPreviewInline]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "categories":
            kwargs['widget'] = forms.SelectMultiple(
                attrs={
                    "class": "w-full bg-blue-50 text-blue-900 rounded-md border border-blue-300 shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500 px-4 py-2",
                    "style": "min-height:120px; max-height:240px; overflow-y:auto;"
                }
            )
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    fieldsets = (
        (None, {
            'fields': (
                'title', 'title_bn', 'slug', 'status', 'description', 'description_bn', 'published_date', 'isbn', 
                'pages', 'cover_image', 'is_available', 'price', 'discounted_price', 'available_copies'
            )
        }),
        ('Author', {
            'fields': (
                'author', 'publisher_name', 'publisher_website_link', 'translator', 'edition', 'language', 'dimensions', 'weight', 'country'
            )
        }),
        (None, {
            'fields': (
                'categories',
            ),
            'classes': ('custom-categories-fieldset',),  # Add a custom class for further CSS targeting if needed
        }),
        ('Status', {
            'fields': (
                'is_new_arrival', 'is_popular', 'is_comming_soon', 'is_best_seller', 'is_active'
            )
        }),
        ('Rating', {
            'fields': (
                'rating', 'rating_count'
            )
        })
    )


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'name_bn', 'slug', 'index_number', 'is_featured', 'is_active')
    list_editable = ('is_featured', 'is_active', 'index_number')
    search_fields = ('name', 'name_bn', 'slug')
    ordering = ('index_number',)
    list_filter = ('is_featured', 'is_active')
    prepopulated_fields = {'slug': ('name',)}

class SpecialPackageBookForm(forms.ModelForm):
    class Meta:
        model = SpecialPackageBook
        fields = '__all__'
        widgets = {
            'book': Select(attrs={
                "class": "w-full bg-gray-100 text-gray-900 rounded-md border border-gray-300 shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500 rounded-md px-4 py-2"
            }),
            'index_number': Input(attrs={
                "placeholder": "Enter Index Number",
                "class": (
                    "w-full bg-gray-100 text-gray-800 rounded-md "
                    "px-4 py-2 border border-gray-300 shadow-sm "
                    "focus:outline-none focus:ring-0 focus:border-none"
                    "rounded-md"
                ),
                "type": "number",
                "min": "0"
            }),
        }

class SpecialPackageBookInline(admin.TabularInline):
    model = SpecialPackageBook
    form = SpecialPackageBookForm
    extra = 1
    autocomplete_fields = ['book']
    show_change_link = True
    classes = ['tab', 'shadow-md', 'rounded-xl', 'p-4', 'bg-gray-500']
    fields = ["book", "index_number"]


@admin.register(SpecialPackage)
class SpecialPackageAdmin(ModelAdmin):
    list_display = ('name', 'name_bn', 'index_number', 'is_active', 'is_featured', 'price')
    list_filter = ('name', 'name_bn', 'is_active', 'is_featured')
    list_editable = ('index_number', 'is_active', 'is_featured', 'price')
    search_fields = ('name', 'name_bn')
    ordering = ('index_number',)

    fieldsets = (
        (None, {
            'fields': (
                'name', 'name_bn', 'description', 'description_bn', 'image',
                'index_number', 'price', 'is_active', 'is_featured'
            )
        }),
    )

    inlines = [SpecialPackageBookInline]

@admin.register(BookReview)
class BookReviewAdmin(ModelAdmin):
    list_display = ('book', 'user', 'rating', 'review', 'created_at')
    list_filter = ('book', 'user', 'rating', 'created_at')
    search_fields = ('book__title', 'user__username', 'review')
    ordering = ('created_at',)
