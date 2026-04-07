from django.urls import path, include
from rest_framework.routers import DefaultRouter
from cart.views import CartView

router = DefaultRouter()
router.register(r'', CartView, basename='cart')

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/update-quantity/<uuid:uuid>/', CartView.as_view({'patch': 'update_quantity'}), name='update-quantity'),
]