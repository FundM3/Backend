from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from main.apps.profile.serializers.serializer import UpdateProfileSerializer, ProfileDetailSerializer, ProfileListSerializer
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

@api_view(['GET'])
def get_profile_view(request, address):
    try:
        profile = Profile.objects.get(user__wallet_address=address)
        serializer = ProfileDetailSerializer(profile, context={'request': request})
        return Response({'status': 'success', 'data': serializer.data})
    except Profile.DoesNotExist:
        return Response({'status': 'error', 'message': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_profile_list(request):
    profiles = Profile.objects.all()
    serializer = ProfileListSerializer(profiles, many=True, context={'request': request})
    return Response({'status': 'success', 'data': serializer.data})
