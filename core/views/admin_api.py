from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta

from user.models import User
from author.models import Author
from book.models import Book, Category, BookReview, SpecialPackage
from order.models import Order, OrderItem
from blog.models import Blog
from core.models import Carousel, Testimonial, Support, GeneralData
from core.utils import build_media_url


class IsAdminUserOrStaff(permissions.BasePermission):
    """Custom permission to check if user is logged in and is staff or superuser."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser))


class AdminDashboardStatsView(APIView):
    permission_classes = [IsAdminUserOrStaff]

    def get(self, request):
        now = timezone.now()
        
        # Summary counts
        total_orders = Order.objects.count()
        pending_orders = Order.objects.filter(status__iexact='pending').count()
        total_revenue = Order.objects.filter(Q(status__iexact='delivered') | Q(status__iexact='completed')).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        total_users = User.objects.count()
        total_books = Book.objects.count()
        total_authors = Author.objects.count()
        total_blogs = Blog.objects.count()
        pending_supports = Support.objects.filter(is_resolved=False).count() if hasattr(Support, 'is_resolved') else Support.objects.count()

        # Monthly Sales Chart Data (last 6 months)
        sales_chart = []
        for i in range(5, -1, -1):
            month_date = now - timedelta(days=i*30)
            month_name = month_date.strftime("%b")
            year = month_date.year
            month = month_date.month

            month_orders = Order.objects.filter(created_at__year=year, created_at__month=month)
            revenue = month_orders.filter(Q(status__iexact='delivered') | Q(status__iexact='completed')).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
            order_count = month_orders.count()

            sales_chart.append({
                "month": month_name,
                "revenue": float(revenue),
                "orders": order_count
            })

        # Recent Orders (last 5)
        recent_orders_qs = Order.objects.select_related('user').order_by('-created_at')[:5]
        recent_orders = []
        for order in recent_orders_qs:
            user_name = order.user.get_full_name() if order.user else (getattr(order, 'customer_name', 'Guest') or 'Guest')
            recent_orders.append({
                "id": order.id,
                "order_id": getattr(order, 'order_id', str(order.id)),
                "customer": user_name,
                "total_price": float(order.total_amount) if hasattr(order, 'total_amount') and order.total_amount else 0.0,
                "status": getattr(order, 'status', 'Pending'),
                "created_at": order.created_at.strftime("%d %b %Y, %H:%M") if hasattr(order, 'created_at') and order.created_at else ""
            })

        # Top Books
        top_books_qs = Book.objects.all().order_by('-id')[:5]
        top_books = []
        for b in top_books_qs:
            top_books.append({
                "id": b.id,
                "title": b.title,
                "price": float(b.price) if b.price else 0.0,
                "stock": getattr(b, 'available_copies', 0),
                "cover_image": build_media_url(b.cover_image) if hasattr(b, 'cover_image') and b.cover_image else None
            })

        return Response({
            "total_revenue": float(total_revenue),
            "total_orders": total_orders,
            "pending_orders": pending_orders,
            "total_users": total_users,
            "total_books": total_books,
            "total_authors": total_authors,
            "total_blogs": total_blogs,
            "pending_supports": pending_supports,
            "sales_chart": sales_chart,
            "recent_orders": recent_orders,
            "top_books": top_books
        })


class AdminUsersViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUserOrStaff]
    queryset = User.objects.all().order_by('-id')

    def list(self, request, *args, **kwargs):
        search = request.query_params.get('search', '')
        qs = self.get_queryset()
        if search:
            qs = qs.filter(Q(email__icontains=search) | Q(full_name__icontains=search) | Q(username__icontains=search))
        
        users_data = []
        for user in qs:
            users_data.append({
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "full_name": user.full_name or user.username,
                "phone_number": str(user.phone_number) if user.phone_number else "",
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,
                "is_active": user.is_active,
                "date_joined": user.date_joined.strftime("%d %b %Y") if user.date_joined else ""
            })
        return Response(users_data)

    def retrieve(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            return Response({
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "full_name": user.full_name,
                "phone_number": str(user.phone_number) if user.phone_number else "",
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,
                "is_active": user.is_active,
                "date_joined": user.date_joined.strftime("%d %b %Y") if user.date_joined else ""
            })
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

    def partial_update(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            data = request.data
            if 'is_staff' in data:
                user.is_staff = data['is_staff']
            if 'is_superuser' in data:
                user.is_superuser = data['is_superuser']
            if 'is_active' in data:
                user.is_active = data['is_active']
            if 'full_name' in data:
                user.full_name = data['full_name']
            if 'phone_number' in data:
                user.phone_number = data['phone_number']
            user.save()
            return Response({"message": "User updated successfully"})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

    def destroy(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            if user.is_superuser:
                return Response({"error": "Cannot delete superuser"}, status=400)
            user.delete()
            return Response({"message": "User deleted successfully"})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)


class AdminAuthorsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUserOrStaff]
    queryset = Author.objects.all().order_by('-id')

    def list(self, request, *args, **kwargs):
        authors = self.get_queryset()
        search = request.query_params.get('search', '')
        if search:
            authors = authors.filter(
                Q(name__icontains=search) | Q(name_bn__icontains=search) | Q(email__icontains=search)
            )
        
        data = []
        for author in authors:
            picture_url = build_media_url(author.profile_picture) if hasattr(author, 'profile_picture') and author.profile_picture else None
            data.append({
                "id": author.id,
                "user_id": author.user_id if hasattr(author, 'user_id') else None,
                "name": author.name or "",
                "name_bn": author.name_bn or "",
                "slug": author.slug or "",
                "email": author.email or "",
                "description": author.description or "",
                "description_bn": author.description_bn or "",
                "bio": author.description or "",
                "bio_bn": author.description_bn or "",
                "phone_number": str(author.phone_number) if author.phone_number else "",
                "address": author.address or "",
                "city": author.city or "",
                "state": author.state or "",
                "country": author.country or "",
                "postal_code": author.postal_code or "",
                "is_active": author.is_active if hasattr(author, 'is_active') else True,
                "profile_picture": picture_url,
                "image": picture_url,
                "created_at": author.created_at.strftime("%d %b %Y") if hasattr(author, 'created_at') and author.created_at else ""
            })
        return Response(data)

    def create(self, request):
        user_id = request.data.get('user_id') or request.data.get('user')
        name = request.data.get('name')
        name_bn = request.data.get('name_bn', '')
        custom_slug = request.data.get('slug', '')
        email = request.data.get('email', '')
        description = request.data.get('description', '') or request.data.get('bio', '')
        description_bn = request.data.get('description_bn', '') or request.data.get('bio_bn', '')
        phone_number = request.data.get('phone_number', '')
        address = request.data.get('address', '')
        city = request.data.get('city', '')
        state = request.data.get('state', '')
        country = request.data.get('country', '')
        postal_code = request.data.get('postal_code', '')
        is_active_val = request.data.get('is_active', 'true')
        is_active = is_active_val.lower() == 'true' if isinstance(is_active_val, str) else bool(is_active_val)
        
        profile_picture = request.FILES.get('profile_picture') or request.FILES.get('image')

        from django.utils.text import slugify
        slug = custom_slug.strip() if custom_slug else (slugify(name) if name else 'author')
        base_slug = slug
        count = 1
        while Author.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{count}"
            count += 1

        author_data = {
            "name": name,
            "name_bn": name_bn,
            "slug": slug,
            "email": email,
            "description": description,
            "description_bn": description_bn,
            "address": address,
            "city": city,
            "state": state,
            "country": country,
            "postal_code": postal_code,
            "is_active": is_active,
        }
        if user_id:
            if Author.objects.filter(user_id=user_id).exists():
                return Response({"error": "This user account is already linked to another author profile."}, status=400)
            author_data["user_id"] = user_id
        if phone_number:
            author_data["phone_number"] = phone_number

        author = Author.objects.create(**author_data)

        if profile_picture:
            author.profile_picture = profile_picture
            author.save()

        return Response({"message": "Author created successfully", "id": author.id}, status=201)

    def partial_update(self, request, pk=None):
        try:
            author = Author.objects.get(pk=pk)
            updatable_fields = [
                'name', 'name_bn', 'slug', 'email', 'description', 'description_bn',
                'address', 'city', 'state', 'country', 'postal_code'
            ]
            for field in updatable_fields:
                if field in request.data:
                    setattr(author, field, request.data[field])

            if 'bio' in request.data and 'description' not in request.data:
                author.description = request.data['bio']
            if 'bio_bn' in request.data and 'description_bn' not in request.data:
                author.description_bn = request.data['bio_bn']

            if 'phone_number' in request.data and request.data['phone_number']:
                author.phone_number = request.data['phone_number']

            if 'user_id' in request.data:
                target_user_id = request.data['user_id'] or None
                if target_user_id and Author.objects.filter(user_id=target_user_id).exclude(pk=author.pk).exists():
                    return Response({"error": "This user account is already linked to another author profile."}, status=400)
                author.user_id = target_user_id

            if 'is_active' in request.data:
                val = request.data['is_active']
                author.is_active = val.lower() == 'true' if isinstance(val, str) else bool(val)

            profile_picture = request.FILES.get('profile_picture') or request.FILES.get('image')
            if profile_picture:
                author.profile_picture = profile_picture

            author.save()
            return Response({"message": "Author updated successfully"})
        except Author.DoesNotExist:
            return Response({"error": "Author not found"}, status=404)

    def destroy(self, request, pk=None):
        try:
            author = Author.objects.get(pk=pk)
            author.delete()
            return Response({"message": "Author deleted successfully"})
        except Author.DoesNotExist:
            return Response({"error": "Author not found"}, status=404)


class AdminBooksViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUserOrStaff]
    queryset = Book.objects.all().prefetch_related('categories').select_related('author').order_by('-id')

    def serialize_book(self, b):
        cat = b.categories.first()
        cat_name = cat.name if cat and hasattr(cat, 'name') else (cat.title if cat and hasattr(cat, 'title') else "")
        return {
            "id": b.id,
            "title": b.title,
            "title_bn": b.title_bn or "",
            "slug": b.slug or "",
            "status": b.status,
            "sku": b.sku or "",
            "description": b.description or "",
            "description_bn": b.description_bn or "",
            "published_date": b.published_date.strftime("%Y-%m-%d") if b.published_date else "",
            "isbn": b.isbn or "",
            "pages": b.pages or 0,
            "cover_image": build_media_url(b.cover_image) if hasattr(b, 'cover_image') and b.cover_image else None,
            "is_available": b.is_available,
            "price": float(b.price) if b.price else 0.0,
            "discount_price": float(b.discounted_price) if hasattr(b, 'discounted_price') and b.discounted_price else None,
            "stock": b.available_copies,
            "author_id": b.author.id if b.author else None,
            "author_name": b.author.name if b.author else "",
            "publisher_name": b.publisher_name or "",
            "publisher_website_link": b.publisher_website_link or "",
            "translator": b.translator or "",
            "edition": b.edition or "",
            "language": b.language or "",
            "dimensions": b.dimensions or "",
            "weight": float(b.weight) if b.weight else None,
            "country": b.country or "",
            "category_id": cat.id if cat else None,
            "category_title": cat_name,
            "is_new_arrival": b.is_new_arrival,
            "is_popular": b.is_popular,
            "is_comming_soon": b.is_comming_soon,
            "is_best_seller": b.is_best_seller,
            "is_featured": b.is_best_seller or b.is_popular,
            "is_active": b.is_active,
        }

    def list(self, request, *args, **kwargs):
        books = self.get_queryset()
        search = request.query_params.get('search', '')
        if search:
            books = books.filter(Q(title__icontains=search) | Q(title_bn__icontains=search) | Q(isbn__icontains=search) | Q(sku__icontains=search))
        
        data = [self.serialize_book(b) for b in books]
        return Response(data)

    def retrieve(self, request, pk=None):
        try:
            b = Book.objects.get(pk=pk)
            return Response(self.serialize_book(b))
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=404)

    def create(self, request):
        data = request.data
        title = data.get('title')
        title_bn = data.get('title_bn', '')
        custom_slug = data.get('slug', '')
        status_val = data.get('status', 'draft')
        sku = data.get('sku', '')
        description = data.get('description', '')
        description_bn = data.get('description_bn', '')
        published_date = data.get('published_date') or timezone.now().date()
        isbn = data.get('isbn', '')
        pages = data.get('pages', 100)
        price = data.get('price', 0)
        discount_price = data.get('discount_price')
        stock = data.get('stock', 0)
        author_id = data.get('author_id')
        publisher_name = data.get('publisher_name', '')
        publisher_website_link = data.get('publisher_website_link', '')
        translator = data.get('translator', '')
        edition = data.get('edition', '')
        language = data.get('language', '')
        dimensions = data.get('dimensions', '')
        weight = data.get('weight')
        country = data.get('country', '')
        category_id = data.get('category_id')

        is_available = data.get('is_available') in [True, 'true', '1']
        is_new_arrival = data.get('is_new_arrival') in [True, 'true', '1']
        is_popular = data.get('is_popular') in [True, 'true', '1']
        is_comming_soon = data.get('is_comming_soon') in [True, 'true', '1']
        is_best_seller = data.get('is_best_seller') in [True, 'true', '1'] or data.get('is_featured') in [True, 'true', '1']
        is_active = data.get('is_active') in [True, 'true', '1'] if 'is_active' in data else True

        cover_image = request.FILES.get('cover_image')

        from django.utils.text import slugify
        slug = slugify(custom_slug) if custom_slug else (slugify(title) if title else 'book')
        base_slug = slug
        count = 1
        while Book.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{count}"
            count += 1

        book = Book.objects.create(
            title=title,
            title_bn=title_bn,
            slug=slug,
            status=status_val,
            sku=sku,
            description=description,
            description_bn=description_bn,
            published_date=published_date,
            isbn=isbn,
            pages=pages if pages else 100,
            price=price,
            discounted_price=discount_price if discount_price else None,
            available_copies=stock if stock else 0,
            author_id=author_id if author_id else None,
            publisher_name=publisher_name,
            publisher_website_link=publisher_website_link if publisher_website_link else None,
            translator=translator,
            edition=edition,
            language=language,
            dimensions=dimensions,
            weight=weight if weight else None,
            country=country,
            is_available=is_available,
            is_new_arrival=is_new_arrival,
            is_popular=is_popular,
            is_comming_soon=is_comming_soon,
            is_best_seller=is_best_seller,
            is_active=is_active
        )
        if category_id:
            book.categories.set([category_id])
        if cover_image and hasattr(book, 'cover_image'):
            book.cover_image = cover_image
            book.save()

        return Response({"message": "Book created successfully", "id": book.id}, status=201)

    def partial_update(self, request, pk=None):
        try:
            book = Book.objects.get(pk=pk)
            data = request.data

            fields = [
                'title', 'title_bn', 'slug', 'status', 'sku', 'description', 'description_bn',
                'published_date', 'isbn', 'pages', 'price', 'publisher_name',
                'publisher_website_link', 'translator', 'edition', 'language',
                'dimensions', 'weight', 'country'
            ]
            for f in fields:
                if f in data:
                    val = data[f]
                    if val == '' and f in ['discounted_price', 'weight', 'publisher_website_link']:
                        val = None
                    setattr(book, f, val)

            if 'discount_price' in data:
                book.discounted_price = data['discount_price'] if data['discount_price'] else None
            if 'stock' in data:
                book.available_copies = data['stock']
            if 'author_id' in data:
                book.author_id = data['author_id'] or None

            if 'is_available' in data:
                book.is_available = data['is_available'] in [True, 'true', '1']
            if 'is_new_arrival' in data:
                book.is_new_arrival = data['is_new_arrival'] in [True, 'true', '1']
            if 'is_popular' in data:
                book.is_popular = data['is_popular'] in [True, 'true', '1']
            if 'is_comming_soon' in data:
                book.is_comming_soon = data['is_comming_soon'] in [True, 'true', '1']
            if 'is_best_seller' in data or 'is_featured' in data:
                val = data.get('is_best_seller', data.get('is_featured'))
                book.is_best_seller = val in [True, 'true', '1']
            if 'is_active' in data:
                book.is_active = data['is_active'] in [True, 'true', '1']

            if 'category_id' in data:
                if data['category_id']:
                    book.categories.set([data['category_id']])
                else:
                    book.categories.clear()

            if 'cover_image' in request.FILES:
                book.cover_image = request.FILES['cover_image']

            book.save()
            return Response({"message": "Book updated successfully"})
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=404)

    def destroy(self, request, pk=None):
        try:
            book = Book.objects.get(pk=pk)
            book.delete()
            return Response({"message": "Book deleted successfully"})
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=404)


class AdminCategoriesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUserOrStaff]
    queryset = Category.objects.all().order_by('-id')

    def list(self, request, *args, **kwargs):
        categories = self.get_queryset()
        data = []
        for c in categories:
            cat_title = getattr(c, 'name', getattr(c, 'title', ''))
            cat_title_bn = getattr(c, 'name_bn', getattr(c, 'title_bn', ''))
            data.append({
                "id": c.id,
                "title": cat_title,
                "title_bn": cat_title_bn,
                "slug": c.slug,
                "icon": build_media_url(c.image) if hasattr(c, 'image') and c.image else (build_media_url(c.icon) if hasattr(c, 'icon') and c.icon else None)
            })
        return Response(data)

    def create(self, request):
        title = request.data.get('title')
        title_bn = request.data.get('title_bn', '')
        icon = request.FILES.get('icon')

        from django.utils.text import slugify
        slug = slugify(title) if title else 'category'
        base_slug = slug
        count = 1
        while Category.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{count}"
            count += 1

        cat = Category.objects.create(name=title, name_bn=title_bn, slug=slug)
        if icon and hasattr(cat, 'image'):
            cat.image = icon
            cat.save()
        return Response({"message": "Category created successfully", "id": cat.id}, status=201)

    def partial_update(self, request, pk=None):
        try:
            cat = Category.objects.get(pk=pk)
            if 'title' in request.data:
                cat.name = request.data['title']
            if 'title_bn' in request.data:
                cat.name_bn = request.data['title_bn']
            if 'icon' in request.FILES and hasattr(cat, 'image'):
                cat.image = request.FILES['icon']
            cat.save()
            return Response({"message": "Category updated successfully"})
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=404)

    def destroy(self, request, pk=None):
        try:
            cat = Category.objects.get(pk=pk)
            cat.delete()
            return Response({"message": "Category deleted successfully"})
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=404)


class AdminOrdersViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUserOrStaff]
    queryset = Order.objects.all().order_by('-id')

    def list(self, request, *args, **kwargs):
        status_filter = request.query_params.get('status', '')
        search = request.query_params.get('search', '')

        qs = self.get_queryset()
        if status_filter:
            qs = qs.filter(status__iexact=status_filter)
        if search:
            qs = qs.filter(Q(id__icontains=search) | Q(order_id__icontains=search) | Q(user__full_name__icontains=search) | Q(user__email__icontains=search))

        data = []
        for order in qs:
            user_name = order.user.get_full_name() if order.user else "Guest"
            user_email = order.user.email if order.user else ""
            data.append({
                "id": order.id,
                "order_id": order.order_id,
                "customer_name": user_name,
                "customer_email": user_email,
                "total_price": float(order.total_amount) if hasattr(order, 'total_amount') and order.total_amount else 0.0,
                "status": getattr(order, 'status', 'Pending'),
                "payment_method": "Online / COD",
                "created_at": order.created_at.strftime("%d %b %Y, %H:%M") if hasattr(order, 'created_at') and order.created_at else ""
            })
        return Response(data)

    def retrieve(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk)
            user_name = order.user.get_full_name() if order.user else "Guest"
            user_email = order.user.email if order.user else ""
            
            items = []
            if hasattr(order, 'items'):
                for item in order.items.all():
                    items.append({
                        "id": item.id,
                        "book_title": item.book.title if hasattr(item, 'book') and item.book else "",
                        "quantity": item.quantity if hasattr(item, 'quantity') else 1,
                        "price": float(item.price) if hasattr(item, 'price') and item.price else 0.0
                    })

            return Response({
                "id": order.id,
                "order_id": order.order_id,
                "customer_name": user_name,
                "customer_email": user_email,
                "customer_phone": str(order.user.phone_number) if order.user and order.user.phone_number else "",
                "shipping_address": str(order.shipping_address) if order.shipping_address else "",
                "total_price": float(order.total_amount) if hasattr(order, 'total_amount') and order.total_amount else 0.0,
                "status": getattr(order, 'status', 'Pending'),
                "payment_method": "Online / COD",
                "created_at": order.created_at.strftime("%d %b %Y, %H:%M") if hasattr(order, 'created_at') and order.created_at else "",
                "items": items
            })
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

    def partial_update(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk)
            if 'status' in request.data:
                order.status = request.data['status']
                order.save()
            return Response({"message": "Order status updated successfully"})
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)


class AdminBlogsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUserOrStaff]
    queryset = Blog.objects.all().order_by('-id')

    def list(self, request, *args, **kwargs):
        blogs = self.get_queryset()
        data = []
        for b in blogs:
            data.append({
                "id": b.id,
                "title": b.title,
                "title_bn": getattr(b, 'title_bn', ''),
                "slug": b.slug,
                "image": build_media_url(b.image) if hasattr(b, 'image') and b.image else None,
                "created_at": b.created_at.strftime("%d %b %Y") if hasattr(b, 'created_at') and b.created_at else ""
            })
        return Response(data)

    def create(self, request):
        title = request.data.get('title')
        title_bn = request.data.get('title_bn', '')
        content = request.data.get('content', '')
        content_bn = request.data.get('content_bn', '')
        image = request.FILES.get('image')

        from django.utils.text import slugify
        slug = slugify(title) if title else 'blog'
        base_slug = slug
        count = 1
        while Blog.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{count}"
            count += 1

        blog = Blog.objects.create(
            title=title,
            title_bn=title_bn,
            slug=slug,
            content=content,
            content_bn=content_bn
        )
        if image and hasattr(blog, 'image'):
            blog.image = image
            blog.save()
        return Response({"message": "Blog created successfully", "id": blog.id}, status=201)

    def destroy(self, request, pk=None):
        try:
            blog = Blog.objects.get(pk=pk)
            blog.delete()
            return Response({"message": "Blog deleted successfully"})
        except Blog.DoesNotExist:
            return Response({"error": "Blog not found"}, status=404)


class AdminCarouselsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUserOrStaff]
    queryset = Carousel.objects.all().order_by('-id')

    def list(self, request, *args, **kwargs):
        carousels = self.get_queryset()
        data = []
        for c in carousels:
            data.append({
                "id": c.id,
                "title": getattr(c, 'title', ''),
                "title_bn": getattr(c, 'title_bn', ''),
                "image": build_media_url(c.image) if hasattr(c, 'image') and c.image else None,
                "link": getattr(c, 'link', '')
            })
        return Response(data)

    def create(self, request):
        title = request.data.get('title', '')
        title_bn = request.data.get('title_bn', '')
        link = request.data.get('link', '')
        image = request.FILES.get('image')

        c = Carousel.objects.create(title=title, title_bn=title_bn, link=link)
        if image and hasattr(c, 'image'):
            c.image = image
            c.save()
        return Response({"message": "Carousel banner created successfully", "id": c.id}, status=201)

    def destroy(self, request, pk=None):
        try:
            c = Carousel.objects.get(pk=pk)
            c.delete()
            return Response({"message": "Carousel banner deleted successfully"})
        except Carousel.DoesNotExist:
            return Response({"error": "Carousel banner not found"}, status=404)


class AdminTestimonialsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUserOrStaff]
    queryset = Testimonial.objects.all().order_by('-id')

    def list(self, request, *args, **kwargs):
        testimonials = self.get_queryset()
        data = []
        for t in testimonials:
            data.append({
                "id": t.id,
                "name": getattr(t, 'name', ''),
                "designation": getattr(t, 'designation', ''),
                "comment": getattr(t, 'comment', ''),
                "rating": getattr(t, 'rating', 5),
                "image": build_media_url(t.image) if hasattr(t, 'image') and t.image else None
            })
        return Response(data)

    def destroy(self, request, pk=None):
        try:
            t = Testimonial.objects.get(pk=pk)
            t.delete()
            return Response({"message": "Testimonial deleted successfully"})
        except Testimonial.DoesNotExist:
            return Response({"error": "Testimonial not found"}, status=404)


class AdminSupportViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUserOrStaff]
    queryset = Support.objects.all().order_by('-id')

    def list(self, request, *args, **kwargs):
        tickets = self.get_queryset()
        data = []
        for s in tickets:
            data.append({
                "id": s.id,
                "name": getattr(s, 'name', ''),
                "email": getattr(s, 'email', ''),
                "subject": getattr(s, 'subject', ''),
                "message": getattr(s, 'message', ''),
                "is_resolved": getattr(s, 'is_resolved', False),
                "created_at": s.created_at.strftime("%d %b %Y") if hasattr(s, 'created_at') and s.created_at else ""
            })
        return Response(data)

    def partial_update(self, request, pk=None):
        try:
            s = Support.objects.get(pk=pk)
            if 'is_resolved' in request.data and hasattr(s, 'is_resolved'):
                s.is_resolved = request.data['is_resolved']
                s.save()
            return Response({"message": "Support ticket updated successfully"})
        except Support.DoesNotExist:
            return Response({"error": "Ticket not found"}, status=404)


class AdminGeneralDataView(APIView):
    permission_classes = [IsAdminUserOrStaff]

    def get(self, request):
        gd = GeneralData.objects.first()
        if not gd:
            return Response({})
        return Response({
            "site_title": getattr(gd, 'site_title', 'Readers Publication'),
            "contact_email": getattr(gd, 'contact_email', ''),
            "contact_phone": getattr(gd, 'contact_phone', ''),
            "address": getattr(gd, 'address', ''),
            "facebook_url": getattr(gd, 'facebook_url', ''),
            "youtube_url": getattr(gd, 'youtube_url', ''),
            "instagram_url": getattr(gd, 'instagram_url', '')
        })

    def put(self, request):
        gd = GeneralData.objects.first()
        if not gd:
            gd = GeneralData.objects.create()
        
        data = request.data
        for field in ['site_title', 'contact_email', 'contact_phone', 'address', 'facebook_url', 'youtube_url', 'instagram_url']:
            if field in data and hasattr(gd, field):
                setattr(gd, field, data[field])
        gd.save()
        return Response({"message": "General settings updated successfully"})
