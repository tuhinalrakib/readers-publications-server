from user.models import User

def dashboard_callback(request, context):
    context = {
        **context,
        "total_users": User.objects.count(),
    }
    return context