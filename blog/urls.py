from django.urls import path
from .views import BlogListReadView, BlogDetailReadView

urlpatterns = [
    path('api/v1/list/', BlogListReadView.as_view(), name='blog-list-read'),
    path('api/v1/detail/<slug:slug>/', BlogDetailReadView.as_view(), name='blog-detail-read'),
]