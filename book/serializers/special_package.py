from rest_framework import serializers
from book.models import SpecialPackage
from django.conf import settings

class SpecialPackageSerializerListRead(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(required=False)

    class Meta:
        model = SpecialPackage
        fields = [
            'uuid', 'image'
        ]

    def get_image(self, obj):
        if obj.image:
            return f"{settings.BACKEND_SITE_HOST}{obj.image.url}"
        return None

    
class SpecialPackageSerializerDetailRead(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(required=False)
    books = serializers.SerializerMethodField(required=False)
    total_price = serializers.SerializerMethodField(required=False)
    
    class Meta:
        model = SpecialPackage
        fields = [
            'uuid', 'name', 'name_bn', 'description', 'description_bn', 'image', 'price', 'books', 'total_price'
        ]

    def get_image(self, obj):
        if obj.image:
            return f"{settings.BACKEND_SITE_HOST}{obj.image.url}"
        return None

    def get_books(self, obj):
        books = obj.package_books.filter(is_active=True).order_by('index_number')
        books_data = []
        for book in books:
            books_data.append({
                "id": book.id,
                "title": book.book.title,
                "title_bn": book.book.title_bn,
                "slug": book.book.slug,
                "author_full_name": book.book.author.name,
                "author_full_name_bn": book.book.author.name_bn,
                "author_slug": book.book.author.slug,
                "price": book.book.price,
                "discounted_price": book.book.discounted_price,
                "rating": book.book.rating,
                "rating_count": book.book.rating_count,
                "cover_image": f"{settings.BACKEND_SITE_HOST}{book.book.cover_image.url}" if book.book.cover_image else None
            })
        return books_data
    
    def get_total_price(self, obj):
        total_price = 0
        for book in obj.package_books.filter(is_active=True):
            total_price += book.book.get_book_price()
        return total_price
    
    