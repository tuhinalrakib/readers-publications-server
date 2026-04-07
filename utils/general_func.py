from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from twilio.rest import Client


def broadcast_sms(message_to_broadcast, to_numbers):
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        for recipient in to_numbers:
            if recipient:
                client.messages.create(to=recipient,
                                        from_=settings.TWILIO_NUMBER,
                                        body=message_to_broadcast)
        return True
    except Exception as e:
        print("error in broadcast_sms", e)
        return False


def send_email(subject, to_email, html_content, text_content="", context={}):
    try:
        from_email = settings.FROM_EMAIL
        msg = EmailMultiAlternatives(
            subject,
            text_content,
            from_email,
            [
                to_email,
            ],
        )

        html_content = render_to_string(html_content, context)

        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return True
    except Exception as e:
        return False
