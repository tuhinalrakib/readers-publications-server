from .registration import UserRegistrationAPIView
from .registration_with_google import GoogleLoginView
from .jwt_auth import CustomTokenObtainPairView 
from .forgot_password import ForgotPasswordAPIView, UpdatePasswordAPIView
from .user_profile import UserProfileView
from .book_wishlist import UserBookWishListAPIView
from .user_reviews import UserReviewsView