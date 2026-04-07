from rest_framework import serializers
from cart.models import Cart
from django.conf import settings

class CartSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['uuid', 'user', 'book', 'quantity']

        extra_kwargs = {
            'uuid': {'read_only': True},
        }

    def create(self, validated_data):
        user = validated_data.get('user')
        book = validated_data.get('book')
        quantity = validated_data.get('quantity')

        if Cart.objects.filter(user=user, book=book).exists():
            cart = Cart.objects.get(user=user, book=book)
            cart.quantity = quantity
            cart.save()
            return cart

        cart = Cart.objects.create(user=user, book=book, quantity=quantity)
        return cart

class CartSerializerRead(serializers.ModelSerializer):
    book_details = serializers.SerializerMethodField()
    author_details = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            'uuid',
            'quantity',
            'book_details',
            'author_details',
            'is_selected',
        ]

    def get_book_details(self, obj):
        return {
            'id': obj.book.id,
            'slug': obj.book.slug,
            'title': obj.book.title,
            'title_bn': obj.book.title_bn,
            'cover_image': f"{settings.BACKEND_SITE_HOST}{obj.book.cover_image.url}" if obj.book.cover_image else None,
            "price": obj.book.price,
            "discounted_price": obj.book.discounted_price,
            "is_active": obj.book.is_active,
            'is_available': obj.book.is_available
        }
    
    def get_author_details(self, obj):
        return {
            'id': obj.book.author.id,
            'name': obj.book.author.name,
            'name_bn': obj.book.author.name_bn,
            'slug': obj.book.author.slug,
        }
    
