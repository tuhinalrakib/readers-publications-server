import requests
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.conf import settings

from typing import Dict, Any


def generate_tokens_for_user(user):
    serializer = TokenObtainPairSerializer()
    token_data = serializer.get_token(user)
    access_token = token_data.access_token
    refresh_token = token_data
    return access_token, refresh_token

def google_get_user_info(*, access_token:  str) -> Dict[str, Any]:
    response = requests.get(
        settings.GOOGLE_USER_INFO_URL,
        params={'access_token': access_token}
    )                   
    if not response.ok:
        raise Exception("Failed to obtain user info from Google.")

    return response.json()
