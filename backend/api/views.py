from django.http import JsonResponse

def welcome(request):
    data = {
        "message": "Welcome to the Django API!"
    }
    return JsonResponse(data)

