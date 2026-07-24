"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from user.views import CustomTokenObtainPairView as TokenObtainPairView
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from core.views.home import home

schema_view = get_schema_view(
   openapi.Info(
      title="Readers Publications - API",
      default_version='v1',
      description="API documentation for phimart e-commerce web application",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="eng.tuhin77@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


from rest_framework.routers import DefaultRouter
from core.views.admin_api import (
    AdminDashboardStatsView, AdminUsersViewSet, AdminAuthorsViewSet,
    AdminBooksViewSet, AdminCategoriesViewSet, AdminOrdersViewSet,
    AdminBlogsViewSet, AdminCarouselsViewSet, AdminTestimonialsViewSet,
    AdminSupportViewSet, AdminGeneralDataView
)

admin_router = DefaultRouter()
admin_router.register(r'users', AdminUsersViewSet, basename='admin-users')
admin_router.register(r'authors', AdminAuthorsViewSet, basename='admin-authors')
admin_router.register(r'books', AdminBooksViewSet, basename='admin-books')
admin_router.register(r'categories', AdminCategoriesViewSet, basename='admin-categories')
admin_router.register(r'orders', AdminOrdersViewSet, basename='admin-orders')
admin_router.register(r'blogs', AdminBlogsViewSet, basename='admin-blogs')
admin_router.register(r'carousels', AdminCarouselsViewSet, basename='admin-carousels')
admin_router.register(r'testimonials', AdminTestimonialsViewSet, basename='admin-testimonials')
admin_router.register(r'support', AdminSupportViewSet, basename='admin-support')

urlpatterns = [
    path("", home),
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Frontend Admin APIs
    path('api/v1/admin/dashboard-stats/', AdminDashboardStatsView.as_view(), name='admin-dashboard-stats'),
    path('api/v1/admin/general-settings/', AdminGeneralDataView.as_view(), name='admin-general-settings'),
    path('api/v1/admin/', include(admin_router.urls)),

    path('user/', include('user.urls')),
    path('book/', include('book.urls')),    
    path('core/', include('core.urls')),
    path('blog/', include('blog.urls')),
    path('author/', include('author.urls')),
    path('cart/', include('cart.urls')),
    path('shipping-address/', include('shipping.urls')),
    path('order/', include('order.urls')),
    # ckeditor5
    path("ckeditor5/", include('django_ckeditor_5.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

