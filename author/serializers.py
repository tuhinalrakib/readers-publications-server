from rest_framework import serializers
from .models import Author
from django.db.models import Avg, Count, Sum
from book.serializers.book import BookSerializerListRead

class AuthorSerializerListRead(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()
    books = serializers.SerializerMethodField()
   
    class Meta:
        model = Author
        fields = [
            'id', 'slug', 'name', 'name_bn', 'profile_picture', 'tags', "description", "description_bn", "rating", "rating_count", "books"
        ]

    def get_profile_picture(self, obj):
        if obj.profile_picture:
            return self.context['request'].build_absolute_uri(obj.profile_picture.url)
        return None
    
    def get_tags(self, obj):
        tags = obj.tags.filter(is_active=True).values("id", "name", "name_bn")
        return tags


    def get_rating(self, obj):
        rating = obj.books.aggregate(Avg('rating'))['rating__avg']
        if rating:  
            return f"{rating:.1f}"
        return 0
    
    def get_rating_count(self, obj):
        rating_count = obj.books.aggregate(Sum('rating_count'))['rating_count__sum']
        if rating_count:
            return rating_count
        return 0
    
    def get_books(self, obj):
        books = obj.books.filter(is_active=True).count()
        return books
    

class AuthorSerializerDetailRead(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()
    book_list = serializers.SerializerMethodField()
   
    class Meta:
        model = Author
        fields = [
            'id', 'slug', 'name', 'name_bn', 'profile_picture', "country", 'tags', "description", "description_bn", "rating", "rating_count", "book_list"
        ]

    def get_profile_picture(self, obj):
        if obj.profile_picture:
            return self.context['request'].build_absolute_uri(obj.profile_picture.url)
        return None
    
    def get_tags(self, obj):
        tags = obj.tags.filter(is_active=True).values("id", "name", "name_bn")
        return tags


    def get_rating(self, obj):
        rating = obj.books.aggregate(Avg('rating'))['rating__avg']
        if rating:  
            return f"{rating:.1f}"
        return 0
    
    def get_rating_count(self, obj):
        rating_count = obj.books.aggregate(Sum('rating_count'))['rating_count__sum']
        if rating_count:
            return rating_count
        return 0
    
    
    def get_book_list(self, obj):
        books = obj.books.filter(is_active=True)
        return BookSerializerListRead(books, many=True, context={"user": obj.user}).data