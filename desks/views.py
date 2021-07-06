from django.contrib.auth import authenticate
from django.db import IntegrityError
from rest_framework.decorators import api_view,authentication_classes,permission_classes,action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from .models import *
from hotdesk.serializers import *
import random, string

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@permission_classes([IsAdminUser])
def create_desk_map(request):
    return Response(ResponseSerializer(GeneralResponse(False,"Hello")))


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_organisation(request):
    org_name = request.data['orgName']
    #Generate id and check unique
    letters = string.ascii_letters
    org_id = ''.join(random.choice(letters) for i in range(16))
    while(len(Organisation.objects.filter(org_id=org_id))):
        letters = string.ascii_letters
        org_id = ''.join(random.choice(letters) for i in range(16))
    print(org_id)
    ## TODO: Create the organisation and then generate serializer to return data
    #Test with a duplicate org id that we don't get infinite loop
    try:

    return Response('Hello')
