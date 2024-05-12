from rest_framework.decorators import api_view
from rest_framework.response import Response
from main.apps.profile.serializers.serializer import UpdateProfileSerializer
from main.apps.profile.models import Profile
from main.apps.user.models import CustomUser


@api_view(['POST'])
def update_profile_view(request):
    email = request.data.get('email')
    address = request.data.get('address')
    
    user = CustomUser.objects.filter(wallet_address=address).first()
    if not user:
        if CustomUser.objects.filter(email=email).exists():
            return Response({'status': 'error', 'message': 'Email already in use'}, status=400)
        user = CustomUser.objects.create_user(email=email, wallet_address=address, is_wallet_connected=True)
    
    if user.email != email:
        return Response({'status': 'error', 'message': 'Email does not match the existing address'}, status=400)
    
    profile, created = Profile.objects.get_or_create(user=user)
    serializer = UpdateProfileSerializer(profile, data=request.data)
    if serializer.is_valid():
        serializer.save()
        message = 'Profile updated successfully' if not created else 'Profile created successfully'
        return Response({'status': 'success', 'message': message})
    else:
        return Response(serializer.errors, status=400)
