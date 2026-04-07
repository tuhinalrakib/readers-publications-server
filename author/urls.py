from django.urls import path
from .views import AuthorViewSet

urlpatterns = [
    path('api/v1/list/', AuthorViewSet.as_view({'get': 'list'}), name='author-list-read'),
    path('api/v1/detail/<slug:slug>/', AuthorViewSet.as_view({'get': 'retrieve'}), name='author-detail-read'),
]