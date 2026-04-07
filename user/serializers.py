from book.models import BookReview
import phonenumbers
from rest_framework import serializers
from django.conf import settings
from user.models import User, UserProfile, BookWishList
from cart.models import Cart
from django.core.validators import EmailValidator

class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone_number', 'password', 'confirm_password']
        extra_kwargs = {
            'email': {'required': True, 'validators': [EmailValidator()]},
            'password': {'write_only': True, 'required': True},
            'confirm_password': {'write_only': True, 'required': True},
            'full_name': {'required': True, 'min_length': 3},
        }

    def validate_phone_number(self, value):
        if not value:
            return value
        
        try:
            parsed_number = phonenumbers.parse(value, None)
            if not phonenumbers.is_valid_number(parsed_number):
                raise serializers.ValidationError("Invalid phone number.")
        except phonenumbers.NumberParseException:
            raise serializers.ValidationError("Invalid phone number format.")
        
        is_exist = User.objects.filter(phone_number=value).exists()
        if is_exist:
            if self.instance and self.instance.phone_number == value:
                return value
            else:
                raise serializers.ValidationError("Phone number already exists.")
        
        return value
    
    def validate_email(self, value):
        is_exist = User.objects.filter(email=value).exists()
        if is_exist:
            if self.instance and self.instance.email == value:
                return value
            else:
                raise serializers.ValidationError("Email already exists.")
        
        return value
        
    def validate(self, data):     
        if data['password'] != data.pop('confirm_password'):
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})

        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        
        return user

class UserProfileSerializerRead(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()
    joined_at = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField()
    cart_items = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = ['id', 'user_id', 'profile_picture', 'address', 'full_name', 'email', 'phone_number', 'joined_at', 'profile_picture', 'cart_items']

    def get_full_name(self, instance):
        return instance.user.full_name if instance.user.full_name else instance.user.username or instance.user.email.split('@')[0]

    def get_email(self, instance):
        return instance.user.email if instance.user.email else ""

    def get_phone_number(self, instance):
        return str(instance.user.phone_number) if instance.user.phone_number else ""
    
    def get_joined_at(self, instance):
        return instance.user.date_joined.strftime("%d %b, %Y")

    def get_profile_picture(self, instance):
        return settings.BACKEND_SITE_HOST + instance.profile_picture.url if instance.profile_picture else None
    
    def get_cart_items(self, instance):
        items = Cart.objects.filter(user=instance.user)
        cart_items = []
        for item in items:
            cart_items.append({
                "uuid": item.uuid,
                "book_id": item.book.id,
                "quantity": item.quantity            
            })
        return cart_items
    
    def get_user_id(self, instance):
        return instance.user.id

class UserBookWishListSerializerRead(serializers.ModelSerializer):
    book_id = serializers.IntegerField(source='book.id')
    title = serializers.CharField(source='book.title')
    title_bn = serializers.CharField(source='book.title_bn')
    author_name = serializers.CharField(source='book.author.name')
    author_name_bn = serializers.CharField(source='book.author.name_bn')
    author_id = serializers.IntegerField(source='book.author.id')
    author_slug = serializers.CharField(source='book.author.slug')
    price = serializers.DecimalField(source='book.price', max_digits=10, decimal_places=2)
    discount_price = serializers.DecimalField(source='book.discounted_price', max_digits=10, decimal_places=2)
    cover_image = serializers.SerializerMethodField()
    slug = serializers.CharField(source='book.slug')

    class Meta:
        model = BookWishList
        fields = ['id', 'book_id', 'title', 'title_bn', 'author_name', 'author_name_bn', 'author_id', 'author_slug', 'cover_image', 'price', 'discount_price', 'slug']

    def get_cover_image(self, instance):
        return settings.BACKEND_SITE_HOST + instance.book.cover_image.url if instance.book.cover_image else None

class UserReviewsSerializerRead(serializers.ModelSerializer):
    book = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    
    class Meta:
        model = BookReview
        fields = ['id', 'book', 'review', 'rating', 'created_at'] 

    def get_book(self, instance):
        return {
            "id": instance.book.id,
            "title": instance.book.title,
            "title_bn": instance.book.title_bn,
            "slug": instance.book.slug,
            "cover_image": settings.BACKEND_SITE_HOST + instance.book.cover_image.url if instance.book.cover_image else None,
            "author_name": instance.book.author.name,
            "author_name_bn": instance.book.author.name_bn,
            "author_slug": instance.book.author.slug,
        }
    
    def get_created_at(self, instance):
        return instance.created_at.strftime("%d %b, %Y")
    
class UserProfileSerializerUpdate(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.full_name')
    email = serializers.CharField(source='user.email')
    phone_number = serializers.CharField(source='user.phone_number')
    profile_picture = serializers.ImageField(required=False, allow_null=True)
    
    class Meta:
        model = UserProfile
        fields = ['full_name', 'email', 'phone_number', 'profile_picture']
        extra_kwargs = {
            'full_name': {'required': True},
            'email': {'required': True},
            'phone_number': {'required': True},
        }
        
    def update(self, instance, validated_data):
        # Pop the nested user data
        user_data = validated_data.pop('user', {})

        # Update user fields
        user = instance.user
        user.full_name = user_data.get('full_name', user.full_name)
        user.email = user_data.get('email', user.email)
        user.phone_number = user_data.get('phone_number', user.phone_number)
        user.save()

        # Update profile_picture (which is stored in UserProfile)
        profile_picture = validated_data.get('profile_picture')
        
        if profile_picture:
            instance.profile_picture = profile_picture

        instance.save()
        return instance

    
