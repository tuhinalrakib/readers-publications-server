from rest_framework.views import APIView
from user.models import BookWishList
from user.serializers import UserBookWishListSerializerRead
from rest_framework.response import Response
from rest_framework import status
from book.models import Book
from core.pagination import GeneralPagination

class UserBookWishListAPIView(APIView):
    serializer_class = UserBookWishListSerializerRead
    queryset = BookWishList.objects.all()
    
    def get(self, request):
        user = request.user
        
        paginator = GeneralPagination()
        paginator.page_size = 4
        page = paginator.paginate_queryset(BookWishList.objects.filter(user=user), request)
        serializer = self.serializer_class(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def post(self, request):
        try:
            user = request.user
            book_id = request.data.get('book_id')
            if not book_id:
                return Response({"error": "Book ID is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            book = Book.objects.get(id=book_id)
            book_wishlist = BookWishList(user=user, book=book)
            book_wishlist.clean()
            book_wishlist.save()
            return Response("Book added to wishlist successfully", status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, id):
        try:
            user = request.user
            if "book_" in id:
                book_id = id.split("_")[1]
                book_wishlist = BookWishList.objects.get(user=user, book_id=book_id)
            else:
                book_wishlist = BookWishList.objects.get(user=user, id=id)
            book_wishlist.delete()
            return Response("Book removed from wishlist successfully", status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    