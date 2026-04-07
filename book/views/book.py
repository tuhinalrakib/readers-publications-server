from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from book.models import Book, BookPreview
from book.serializers.book import BookSerializerListRead, BookSerializerDetailRead, BookPreviewSerializerListRead, BookReviewSerializerListRead, BookReviewSerializerCreate
from core.pagination import GeneralPagination
from rest_framework.response import Response
from book.models import BookReview
from rest_framework.decorators import api_view
from django.db.models import Q

class BookListAPIView(ListAPIView):
    serializer_class = BookSerializerListRead
    queryset = Book.objects.all()
    pagination_class = GeneralPagination

    def get_queryset(self):
        category = self.request.query_params.getlist("category[]")
        author = self.request.query_params.getlist("author[]")
        price_min = self.request.query_params.get("price[min]")
        price_max = self.request.query_params.get("price[max]")
        search = self.request.query_params.get("search")

        queryset = Book.objects.all()

        # sort by
        sort_by = self.request.query_params.get("sort_by")
        if sort_by == "recent":
            queryset = queryset.order_by('-published_date', '-created_at')
        elif sort_by == "popular":
            queryset = queryset.order_by('-rating', '-created_at')
        elif sort_by == "price_low_to_high":
            queryset = queryset.order_by('price')
        elif sort_by == "price_high_to_low":
            queryset = queryset.order_by('-price')


        if category:
            queryset = queryset.filter(categories__id__in=category).distinct()
        if author:
            queryset = queryset.filter(author__id__in=author).distinct()
        if price_min and int(price_min) > 0:
            price_min = int(price_min)
            queryset = queryset.filter(price__gte=price_min).distinct()
        if price_max and int(price_max) > 0:
            price_max = int(price_max)
            queryset = queryset.filter(price__lte=price_max).distinct()

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(title_bn__icontains=search) | 
                Q(author__name__icontains=search) | 
                Q(author__name_bn__icontains=search) | 
                Q(publisher_name__icontains=search) | 
                Q(categories__name__icontains=search)).distinct()
            
        return queryset.filter(is_active=True)
    
    def paginate_queryset(self, queryset):
        self.pagination_class.page_size = 20
        return super().paginate_queryset(queryset)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.user.is_authenticated:
            context['user'] = self.request.user
        else:
            context['user'] = None
        return context
    
    def get_paginated_response(self, data):
        # If pagination is off, return all data in a single response
        is_pagination_off = self.request.query_params.get('pagination', 'true')
        is_featured = self.request.query_params.get("is_featured")

        # Home pase featured data
        if is_pagination_off == 'false' and is_featured == "true":

            qs = Book.objects.filter(is_active=True).order_by('-published_date')
            new_arrival = qs.filter(is_new_arrival=True)
            popular = qs.filter(is_popular=True)
            comming_soon = qs.filter(is_comming_soon=True)
            best_seller = qs.filter(is_best_seller=True)
            
            if self.request.user.is_authenticated:
                user = self.request.user
            else:
                user = None

            data = {
                "new_arrival": BookSerializerListRead(new_arrival, many=True, context={"user": user}).data,
                "popular": BookSerializerListRead(popular, many=True, context={"user": user}).data,
                "comming_soon": BookSerializerListRead(comming_soon, many=True, context={"user": user}).data,
                "best_seller": BookSerializerListRead(best_seller, many=True, context={"user": user}).data,
            }

            return Response(data)
        return super().get_paginated_response(data)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    

class BookDetailAPIView(RetrieveAPIView):
    serializer_class = BookSerializerDetailRead
    queryset = Book.objects.all()
    lookup_field = "slug"

    def get_object(self):
        return super().get_object()
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    

class BookPreviewAPIView(ListAPIView):
    serializer_class = BookPreviewSerializerListRead
    queryset = BookPreview.objects.all()
    pagination_class = GeneralPagination

    def get_queryset(self): 
        return BookPreview.objects.filter(book_id=self.kwargs['book_id'], is_active=True).order_by('index_number')
    

class BookReviewAPIView(ListAPIView):
    serializer_class = BookReviewSerializerListRead
    queryset = BookReview.objects.all()
    pagination_class = GeneralPagination

    def get_queryset(self):
        return BookReview.objects.filter(book_id=self.kwargs['book_id'], is_active=True).order_by('-created_at')
    
    def paginate_queryset(self, queryset):
        self.pagination_class.page_size = 3
        return super().paginate_queryset(queryset)

class BookReviewCreateAPIView(CreateAPIView):
    serializer_class = BookReviewSerializerCreate
    queryset = BookReview.objects.all()

    def perform_create(self, serializer):
        book_id = self.kwargs['book_id']
        book = Book.objects.get(id=book_id)
        if book.rating_count == 0:
            book.rating_count = 1
        else:
            book.rating_count += 1
        book.rating = (book.rating * (book.rating_count - 1) + serializer.validated_data['rating']) / book.rating_count
        book.save()
        # Create book review
        serializer.save(user=self.request.user, book=book)


@api_view(['GET'])
def get_book_review_distribution(request, book_id):
    reviews = BookReview.objects.filter(book_id=book_id, is_active=True).values('rating')
    
    return Response({
        "1": reviews.filter(rating=1).count(),
        "2": reviews.filter(rating=2).count(),
        "3": reviews.filter(rating=3).count(),
        "4": reviews.filter(rating=4).count(),
        "5": reviews.filter(rating=5).count(),
        "total": reviews.count(),
    })


class BookRelatedAPIView(ListAPIView):
    serializer_class = BookSerializerListRead
    queryset = Book.objects.all()
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.user.is_authenticated:
            context['user'] = self.request.user
        else:
            context['user'] = None
        return context
    
    def get_queryset(self):
        book_id = self.request.query_params.get('book_id')
        book = Book.objects.get(id=book_id)
        categories = book.categories.all()
        author = book.author
        publisher_name = book.publisher_name
        title = book.title

        related_books = Book.objects.filter(
            Q(is_active=True) &
            Q(categories__id__in=categories) |
            Q(author=author) |
            Q(publisher_name=publisher_name) |
            Q(title__icontains=title)
        ).order_by('-published_date').distinct()

        # if related books are less than 10, add more books
        if related_books.count() < 10:
            books = Book.objects.filter(is_active=True, id__not_in=related_books.values_list('id', flat=True)).order_by('-published_date')[:10]
            related_books = related_books | books
        
        return related_books[:10]


