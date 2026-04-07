from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from author.models import Author
from author.serializers import AuthorSerializerListRead, AuthorSerializerDetailRead

class AuthorViewSet(viewsets.ViewSet):
    def list(self, request):
        authors = Author.objects.filter(is_active=True).order_by('user__full_name')
        serializer = AuthorSerializerListRead(authors, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, slug=None):
        try:
            author = Author.objects.get(slug=slug, is_active=True)
            serializer = AuthorSerializerDetailRead(author, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Author.DoesNotExist:
            return Response({"detail": "Author not found."}, status=status.HTTP_404_NOT_FOUND)
