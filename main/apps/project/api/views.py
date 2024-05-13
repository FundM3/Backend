from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import transaction
from main.apps.project.serializers.serializer import CreateProjectSerializer, ProjectDetailSerializer, ProjectListSerializer
from main.apps.project.models import Project
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

@api_view(['GET'])
def get_project_view(request, id):
    try:
        project = Project.objects.get(id=id)
        serializer = ProjectDetailSerializer(project, context={'request': request})
        return Response({'status': 'success', 'data': serializer.data})
    except Project.DoesNotExist:
        return Response({'status': 'error', 'message': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_project_list(request):
    projects = Project.objects.all()
    serializer = ProjectListSerializer(projects, many=True, context={'request': request})
    return Response({'status': 'success', 'data': serializer.data})
