from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from core.models import GeneralData, State, City, Thana
from django.conf import settings

@api_view(['GET'])
def get_general_data(request):
    try:
        general_data = GeneralData.objects.first()
        if not general_data:
            return Response({"error": "General data not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({
            "contact_email": general_data.email,
            "contact_phone": general_data.phone,
            "address": general_data.address,
            "address_bn": general_data.address_bn,
            "delivery_charge": general_data.delivery_charge,
            "website_logo": settings.BACKEND_SITE_HOST + general_data.website_logo.url if general_data.website_logo else None,
            "social_links": {
                "facebook": general_data.facebook,
                "twitter": general_data.twitter,
                "instagram": general_data.instagram,
                "linkedin": general_data.linkedin,
                "youtube": general_data.youtube
            },
            "articles_section": {
                "title": general_data.articles_section_title,
                "title_bn": general_data.articles_section_title_bn,
                "subtitle": general_data.articles_section_subtitle,
                "subtitle_bn": general_data.articles_section_subtitle_bn
            }
        }, status=status.HTTP_200_OK)
    except GeneralData.DoesNotExist:
        return Response({"error": "General data not found"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def get_state_list(request):
    try:
        state_list = State.objects.all().values('id', 'name', 'name_bn')
        return Response(state_list, status=status.HTTP_200_OK)
    except State.DoesNotExist:
        return Response({"error": "State list not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_city_list(request):
    try:
        state_id = request.GET.get('state_id')
        city_list = City.objects.filter(state_id=state_id).values('id', 'name', 'name_bn')
        return Response(city_list, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def get_thana_list(request):
    try:
        city_id = request.GET.get('city_id')
        thana_list = Thana.objects.filter(city_id=city_id).values('id', 'name', 'name_bn')
        return Response(thana_list, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
