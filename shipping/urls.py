from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShippingModelViewSet

router = DefaultRouter()
router.register(r'', ShippingModelViewSet, basename='shipping')

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
