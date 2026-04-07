from django.urls import path
from user.views import UserRegistrationAPIView, GoogleLoginView, ForgotPasswordAPIView, \
    UpdatePasswordAPIView, UserProfileView, UserBookWishListAPIView, UserReviewsView    

urlpatterns = [
    path('api/v1/auth/registration/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('api/v1/auth/google-login/', GoogleLoginView.as_view(), name='google-login'),
    path('api/v1/auth/forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot-password'),
    path('api/v1/auth/update-password/', UpdatePasswordAPIView.as_view(), name='update-password'),

    path('api/v1/user/profile/', UserProfileView.as_view(), name='user-profile'),
    path('api/v1/wishlist/', UserBookWishListAPIView.as_view(), name='user-wishlist'),
    path('api/v1/wishlist/<str:id>/', UserBookWishListAPIView.as_view(), name='user-wishlist-delete'),
    path('api/v1/reviews/', UserReviewsView.as_view(), name='user-reviews'),
]
