from rest_framework.generics import ListAPIView
from book.models import Category
from book.serializers.category import CategorySerializer

class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    pagination_class = None

    def get_queryset(self):
        is_featured = self.request.query_params.get('is_featured', False)
        if is_featured:
            return super().get_queryset().filter(is_active=True, is_featured=True).order_by('index_number')
        return super().get_queryset().filter(is_active=True).order_by('index_number')
    
