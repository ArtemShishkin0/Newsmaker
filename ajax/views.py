from django.http import JsonResponse
from django.contrib.auth.models import Group, User

def validate_data(request):
    username = request.GET.get('user', None)
    email = request.GET.get('email', None)
    response = {
        'username_is_taken': User.objects.filter(username__iexact=username).exists(),
        'email_is_taken': User.objects.filter(email__iexact=email).exists(),
    }
    return JsonResponse(response)
