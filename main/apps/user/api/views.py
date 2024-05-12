from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from main.apps.user.models import CustomUser 
import json


@require_http_methods(["POST"])
def login_view(request):
    data = json.loads(request.body.decode('utf-8'))
    email = data.get('email')
    password = data.get('password')
    
    user = CustomUser.objects.filter(email=email).first()
    if user is not None:
        user = authenticate(request, username=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return JsonResponse({'status': 'success', 'message': 'Login successful'}, status=200)
            else:
                return JsonResponse({'status': 'error', 'message': 'Account is disabled'}, status=401)
        else:
            return JsonResponse({'status': 'error', 'message': 'Password is incorrect'}, status=401)
    else:
        # User does not exist, create a new one
        new_user = CustomUser.objects.create_user(email=email, password=password, is_wallet_connected=False)
        login(request, new_user)
        return JsonResponse({'status': 'success', 'message': 'User created and logged in successfully'}, status=200)
