from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from user.models import User


class CustomAuthBackend(ModelBackend):

    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False

    def authenticate(self, request, email, password):

        user_id = email  # 'email' can be 'email address/phone number'

        try:
            user = User.objects.get(
                Q(email__iexact=user_id) | Q(phone_number__iexact=user_id)
            )

            if user.check_password(password):
                return user

        except User.DoesNotExist:
            return None
