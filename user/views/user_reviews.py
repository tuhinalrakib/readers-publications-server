from book.models import BookReview
from book.serializers.book import BookReviewSerializerListRead
from core.pagination import GeneralPagination
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from user.models.book_wish_list import BookWishList
from user.serializers import UserReviewsSerializerRead

class UserReviewsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserReviewsSerializerRead
    pagination_class = GeneralPagination
    
    def get_queryset(self):
        try:
            if getattr(self,"swagger_fake_view", False):
                BookReview.objects.none
                
            user = self.request.user
            
            if not user.is_authenticated:
                return BookReview.objects.none()
                      
            return BookReview.objects.filter(user=user)
        except BookReview.DoesNotExist:
            return Response({
                "message": "User reviews not found"
            }, status=status.HTTP_404_NOT_FOUND)
