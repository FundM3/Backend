from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from main.apps.contribution.models import Contribution
from main.apps.contribution.serializers.serializer import RecordContributionSerializer, ContributionListSerializer


@api_view(['POST'])
def record_contribution_view(request):
    serializer = RecordContributionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'status': 'success', 'message': 'Contribution recorded successfully'}, status=200)
    else:
        return Response({'status': 'error', 'message': serializer.errors}, status=400)

@api_view(['GET'])
def get_contribution_list(request, address):
    contributions = Contribution.objects.filter(receiver_address=address)
    if contributions.exists():
        serializer = ContributionListSerializer(contributions, many=True, context={'request': request})
        return Response({'status': 'success', 'data': serializer.data}, status=200)
    else:
        return Response({'status': 'success', 'data': []}, status=200)
