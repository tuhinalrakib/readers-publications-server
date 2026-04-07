from rest_framework import serializers
from book.models import Book, Category, BookImage, BookPreview, BookReview
from django.conf import settings

class BookSerializerListRead(serializers.ModelSerializer):
    cover_image = serializers.SerializerMethodField(required=False)
    author_full_name = serializers.SerializerMethodField()
    author_full_name_bn = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    discounted_price = serializers.SerializerMethodField()
    author_id = serializers.SerializerMethodField()
    author_slug = serializers.SerializerMethodField()
    is_in_wishlist = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = [
            'id', 'slug', 'title', 'title_bn', 'author_full_name', 'author_full_name_bn', 'cover_image', 'price', 'discounted_price',
            'rating', 'rating_count', 'is_available', "is_new_arrival", "is_popular", "is_comming_soon", "author_id", "author_slug", "is_in_wishlist"
        ]

    def get_cover_image(self, obj):
        if obj.cover_image:
            return f"{settings.BACKEND_SITE_HOST}{obj.cover_image.url}"
        return None
    
    def get_author_full_name(self, obj):
        return obj.author.name

    def get_author_full_name_bn(self, obj):
        return obj.author.name_bn if obj.author.name_bn else obj.author.name
    
    def get_price(self, obj):
        return int(obj.price)
    
    def get_discounted_price(self, obj):
        return int(obj.discounted_price) if obj.discounted_price else None
    
    def get_author_id(self, obj):
        return obj.author.id
    
    def get_author_slug(self, obj):
        return obj.author.slug
    
    def get_is_in_wishlist(self, obj):
        if self.context.get('user'):
            return obj.wishlist.filter(user=self.context['user']).exists()
        elif self.context.get("request"):
            if self.context.get("request").user.is_authenticated:
                return obj.wishlist.filter(user=self.context['request'].user).exists()
        return False
    
class BookImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(required=False)
    
    class Meta:
        model = BookImage
        fields = ['id', 'image', 'alt_text']

    def get_image(self, obj):
        if obj.image:
            return f"{settings.BACKEND_SITE_HOST}{obj.image.url}"
        return None

class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Category
        fields =  ['name', 'description', 'image']  # or specify fields like ('id', 'name', 'description')

    def get_image(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None
    

class BookSerializerDetailRead(serializers.ModelSerializer):
    cover_image = serializers.SerializerMethodField(required=False)
    author = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    book_images = serializers.SerializerMethodField()
    has_preview_images = serializers.SerializerMethodField()
    can_give_review = serializers.SerializerMethodField()
    is_in_wishlist = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields =  [
            'id', 'slug', 'title', 'title_bn', "rating", "rating_count",
            "is_available", "price", "discounted_price", "publisher_name", "publisher_website_link",
            "pages", "description", "description_bn", "available_copies", "language", "dimensions",
            "weight", "published_date", "cover_image", "author", "categories", "book_images", "edition", "has_preview_images", "can_give_review", "is_in_wishlist"
        ]

    def get_cover_image(self, obj):
        if obj.cover_image:
            return f"{settings.BACKEND_SITE_HOST}{obj.cover_image.url}"
        return None

    def get_author(self, obj):
        return {
            "id": obj.author.id,
            "slug": obj.author.slug,
            "name": obj.author.name,
            "name_bn": obj.author.name_bn,
            "bio": obj.author.description,
            "bio_bn": obj.author.description_bn,
            "profile_picture": f"{settings.BACKEND_SITE_HOST}{obj.author.profile_picture.url}" if obj.author.profile_picture else None,
            "tags": obj.author.tags.filter(is_active=True).values('id', 'name', 'name_bn')
        }
    
    def get_categories(self, obj):
        categories = obj.categories.all()
        categories_data = [
            {
                "id": category.id,
                "name": category.name,
                "name_bn": category.name_bn,
            }
            for category in categories
        ]
        return categories_data

    def get_book_images(self, obj): 
        book_images = obj.images.all()
        book_images_data = [
            {
                "id": book_image.id,
                "image": f"{settings.BACKEND_SITE_HOST}{book_image.image.url}",
                "alt_text": book_image.alt_text,
            }
            for book_image in book_images
        ]
        return book_images_data
    
    def get_has_preview_images(self, obj):
        return obj.previews.filter(is_active=True).count() > 0
    
    def get_can_give_review(self, obj):
        return obj.user_can_give_review(self.context['request'].user)
    
    def get_is_in_wishlist(self, obj):
        if self.context['request'].user and self.context['request'].user.is_authenticated:
            return obj.wishlist.filter(user=self.context['request'].user).exists()
        return False
    
class BookPreviewSerializerListRead(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(required=False)

    class Meta:
        model = BookPreview
        fields = ['id', 'image']

    def get_image(self, obj):
        if obj.image:
            return f"{settings.BACKEND_SITE_HOST}{obj.image.url}"
        return None
    

class BookReviewSerializerListRead(serializers.ModelSerializer):
    user_details = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    class Meta:
        model = BookReview
        fields = ['id', 'review', 'rating', 'user_details', 'created_at']

    def get_user_details(self, obj):
        return {
            "id": obj.user.id,
            "name": obj.user.full_name,
            "profile_picture": f"{settings.BACKEND_SITE_HOST}{obj.user.profile.profile_picture.url}" if hasattr(obj.user, 'profile') and obj.user.profile.profile_picture else None,
        }

    def get_created_at(self, obj):
        return obj.created_at.strftime("%d %b %Y, %I:%M %p")


class BookReviewSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = BookReview
        fields = ['review', 'rating']

