from django.contrib.auth import authenticate
from django.db import IntegrityError
from rest_framework.decorators import api_view,authentication_classes,permission_classes,action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from .models import *
from hotdesk.serializers import *

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@permission_classes([IsAdminUser])
def create_desk_map(request):
    return Response(ResponseSerializer(GeneralResponse(False,"Hello")))
