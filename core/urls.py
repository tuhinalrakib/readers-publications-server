from django.urls import path
from .views import CarouselListViewSet, get_general_data, TestimonialListAPIView, get_state_list, get_city_list, get_thana_list

urlpatterns = [
    # path('api/v1/support/', SupportCreateView.as_view(), name='support-create'),
    path('api/v1/general-data/', get_general_data, name='general-data-retrieve'),
    path('api/v1/home-carousel/', CarouselListViewSet.as_view({'get': 'list'}), name='home-carousel-list'),
    path('api/v1/testimonials/', TestimonialListAPIView.as_view(), name='testimonial-list'),
    path('api/v1/state-list/', get_state_list, name='state-list'),
    path('api/v1/city-list/', get_city_list, name='city-list'),
    path('api/v1/thana-list/', get_thana_list, name='thana-list'),
]