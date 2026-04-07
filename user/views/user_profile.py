from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from user.serializers import UserProfileSerializerRead, UserProfileSerializerUpdate
from user.models import UserProfile

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            user_profile = UserProfile.objects.get(user=user)
            serializer = UserProfileSerializerRead(user_profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response({
                "message": "User profile not found"
            }, status=status.HTTP_404_NOT_FOUND)
            
    def put(self, request, *args, **kwargs):
        try:
            user = request.user
            user_profile = UserProfile.objects.get(user=user)
            serializer = UserProfileSerializerUpdate(user_profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)