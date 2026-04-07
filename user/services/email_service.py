import random
import string
from core.tasks import send_email_task
from user.models import VerificationCode

class EmailService:
    def generate_code(self, length=6):
        while True:
            code = ''.join(random.choices(string.digits, k=length))
            if not VerificationCode.objects.filter(code=code).exists():
                break
        return code

    
    def send_code(self, subject, template, to_email=[], context={}):
        send_email_task.delay(
            to_email,
		    subject,
		    template,
		    context
		)
        return True
