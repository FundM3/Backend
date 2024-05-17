from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from main.apps.user.models import CustomUser 
from main.apps.profile.models import Profile
from main.apps.profile.serializers.serializer import ProfileDetailSerializer
import json


@require_http_methods(["POST"])
def login_view(request):
    data = json.loads(request.body.decode('utf-8'))
    email = data.get('email')
    password = data.get('password')
    
    user = CustomUser.objects.filter(email=email).first()
    if user is None:
        new_user = CustomUser.objects.create_user(email=email, password=password, is_wallet_connected=False)
        login(request, new_user)
        return JsonResponse({
            'status': 'success',
            'message': 'User created and logged in successfully',
            'data': {'address': new_user.wallet_address, 'email': new_user.email}
        }, status=200)

    user = authenticate(request, username=email, password=password)
    if user is None:
        return JsonResponse({'status': 'error', 'message': 'Password is incorrect'}, status=401)

    if not user.is_active:
        return JsonResponse({'status': 'error', 'message': 'Account is disabled'}, status=401)

    login(request, user)
    profile = Profile.objects.filter(user=user).first()
    if profile is None:
        return JsonResponse({
            'status': 'success',
            'message': 'Login successful, but no profile found',
            'data': {'address': user.wallet_address, 'email': user.email}
        }, status=200)

    serializer = ProfileDetailSerializer(profile, context={'request': request})
    return JsonResponse({
        'status': 'success', 
        'message': 'Login successful',
        'data':{'address': serializer.data.get("address"), 'email': serializer.data.get("email")}
    }, status=200)
