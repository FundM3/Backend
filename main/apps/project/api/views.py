from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import transaction
from django.shortcuts import get_object_or_404
from main.apps.project.serializers.serializer import CreateProjectSerializer
from main.apps.profile.models import Profile
from main.apps.user.models import CustomUser


@api_view(['POST'])
@parser_classes((MultiPartParser, FormParser))
def create_project_view(request):
    address = request.data.get('address')
    user = CustomUser.objects.filter(wallet_address=address).select_related('profile').first()
    if not user:
        return Response({'status': 'error', 'message': 'No user found with the provided wallet address'}, status=404)

    if not user.profile or not user.profile.visible:
        return Response({'status': 'error', 'message': 'User profile is not visible or does not exist'}, status=400)

    project_serializer = CreateProjectSerializer(data=request.data)
    
    if project_serializer.is_valid():
        with transaction.atomic():
            project = project_serializer.save(user=user)
        return Response({'status': 'success', 'message': 'Project created successfully', 'project_id': project.pk})
    else:
        return Response({'status': 'error', 'message': project_serializer.errors}, status=400)
