from rest_framework.generics import ListAPIView, RetrieveAPIView
from book.serializers.special_package import SpecialPackageSerializerListRead, SpecialPackageSerializerDetailRead
from book.models import SpecialPackage
from core.pagination import GeneralPagination


class SpecialPackageListAPIView(ListAPIView):
    serializer_class = SpecialPackageSerializerListRead
    queryset = SpecialPackage.objects.all()
    pagination_class = GeneralPagination

    def get_queryset(self):
        is_featured = self.request.GET.get("is_featured", False)
        if is_featured == "true":   
            return SpecialPackage.objects.filter(is_active=True, is_featured=True).order_by('-index_number')
        return SpecialPackage.objects.filter(is_active=True).order_by('-index_number') 
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context



class SpecialPackageDetailAPIView(RetrieveAPIView):
    serializer_class = SpecialPackageSerializerDetailRead
    queryset = SpecialPackage.objects.all()
    lookup_field = 'uuid'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
