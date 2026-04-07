import random
import string
from core.tasks import broadcast_sms_task

class PhoneService:
    def generate_code(self, length=6):
        return ''.join(random.choices(string.digits, k=length))

    def send_code(self, user, message, to_numbers):
        broadcast_sms_task.delay(message, to_numbers)


