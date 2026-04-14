from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "message": "Readers Publication API is running 🚀"
    })