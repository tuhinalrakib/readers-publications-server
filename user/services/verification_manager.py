from user.models import VerificationCode

class VerificationManager:
    def __init__(self, service, type, **kwargs):
        self.service = service
        self.type = type
        self.kwargs = kwargs

    def create_and_send_code(self, user, code):
        self.service.send_code(
            **self.kwargs
        )
        VerificationCode.objects.filter(user=user, type=self.type).delete()
        VerificationCode.objects.create(user=user, code=code, type=self.type)

