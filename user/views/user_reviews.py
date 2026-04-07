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

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            paginator = GeneralPagination()
            paginator.page_size = 4
            page = paginator.paginate_queryset(BookReview.objects.filter(user=user), request)
            serializer = UserReviewsSerializerRead(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except BookReview.DoesNotExist:
            return Response({
                "message": "User reviews not found"
            }, status=status.HTTP_404_NOT_FOUND)

