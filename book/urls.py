from django.urls import path
from book.views.category import CategoryListAPIView
from book.views.book import BookListAPIView, BookDetailAPIView, BookPreviewAPIView, BookReviewAPIView, \
    BookReviewCreateAPIView, get_book_review_distribution, BookRelatedAPIView
from book.views.special_package import SpecialPackageListAPIView, SpecialPackageDetailAPIView


urlpatterns = [
    path('api/v1/categories/', CategoryListAPIView.as_view(), name='book-categories-list'),
    path('api/v1/list/', BookListAPIView.as_view(), name='book-list'),
    path('api/v1/special-packages/', SpecialPackageListAPIView.as_view(), name='special-package-list'),
    path('api/v1/special-packages/<uuid:uuid>/', SpecialPackageDetailAPIView.as_view(), name='special-package-detail'),
    path('api/v1/detail/<slug:slug>/', BookDetailAPIView.as_view(), name='book-detail'),
    path('api/v1/previews/<int:book_id>/', BookPreviewAPIView.as_view(), name='book-previews'),
    path('api/v1/reviews/<int:book_id>/', BookReviewAPIView.as_view(), name='book-reviews'),
    path('api/v1/reviews/create/<int:book_id>/', BookReviewCreateAPIView.as_view(), name='book-review-create'),
    path('api/v1/reviews/distribution/<int:book_id>/', get_book_review_distribution, name='book-reviews-distribution'),
    path('api/v1/related-books/', BookRelatedAPIView.as_view(), name='book-related'),
]
