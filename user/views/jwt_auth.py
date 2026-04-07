from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from user.serializers import UserProfileSerializerRead

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            profile_serializer = UserProfileSerializerRead(user.profile)
            
            # Update last login timestamp
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
            
            return Response({
            "access_token": str(serializer.validated_data['access']),
            "refresh_token": str(serializer.validated_data['refresh']),
            "user_info": profile_serializer.data
        }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
