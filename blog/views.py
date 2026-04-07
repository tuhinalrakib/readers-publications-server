from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Blog
from .serializers import BlogSerializerListRead, BlogSerializerDetailRead
from core.pagination import GeneralPagination

class BlogListReadView(ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializerListRead
    pagination_class = GeneralPagination

    def get_queryset(self):
        is_featured = self.request.query_params.get('is_featured', False)
        blogs = Blog.objects.filter(is_active=True, is_featured=is_featured).order_by('-created_at')
        return blogs
    

class BlogDetailReadView(RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializerDetailRead
    lookup_field = 'slug'

    def get_queryset(self):
        slug = self.kwargs['slug']
        return Blog.objects.filter(is_active=True, slug=slug).order_by('-created_at')
