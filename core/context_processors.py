from django.conf import settings


def media_url(request):
    return {
        'media_url': settings.MEDIA_URL
    }


def google_analytics(request):
    return {
        'GOOGLE_ANALYTICS_ID': getattr(settings, 'GOOGLE_ANALYTICS_ID', None)
    }
