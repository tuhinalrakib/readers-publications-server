from django.conf import settings


def build_media_url(file_field):
    if not file_field:
        return None

    url = file_field.url
    if url.startswith(("http://", "https://")):
        return url

    return f"{settings.BACKEND_SITE_URL}{url}"
