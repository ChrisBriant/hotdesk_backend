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
        org = Organisation.objects.create(
            owner = request.user,
            name = org_name,
            org_id = org_id
        )
        OrgEmployee.objects.create(
            employee = request.user,
            organisation = org,
            approved = True
        )
    except Exception as e:
        print(e)
        return Response(ResponseSerializer(GeneralResponse(False,"An error occured adding the organisation")).data, status=status.HTTP_400_BAD_REQUEST)
    orgserializer = OrganisationSerializer(org)
    return Response(orgserializer.data,status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def my_orgs(request):
    my_orgs = OrgEmployee.objects.filter(employee=request.user)
    myorg_serializer = OrgEmployeeSerializer(my_orgs,many=True,context={'user' : request.user})
    return Response(myorg_serializer.data,status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_org(request):
    org_id = request.data['orgId']
    print(org_id)
    try:
        org = Organisation.objects.get(org_id=org_id)
    except Exception as e:
        print(e)
        return Response(ResponseSerializer(GeneralResponse(False,"Organisation not found.")).data, status=status.HTTP_400_BAD_REQUEST)
    try:
        OrgEmployee.objects.create(
            employee = request.user,
            organisation = org,
        )
    except IntegrityError as e:
        return Response(ResponseSerializer(GeneralResponse(False,"You have already requested to join this organisation.")).data, status=status.HTTP_400_BAD_REQUEST)
    return Response(ResponseSerializer(GeneralResponse(True,"Succesfully Joined {} please await approval.".format(org.name))).data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_org(request):
    org_id = request.data['orgId']
    try:
        org_emp = OrgEmployee.objects.get(organisation_id=org_id,employee=request.user)
    except Exception as e:
        print(e)
        return Response(ResponseSerializer(GeneralResponse(False,"Organisation not found.")).data, status=status.HTTP_400_BAD_REQUEST)
    if org_emp.approved:
        orgserializer = OrganisationSerializer(org_emp.organisation,context={'user' : request.user})
    else:
        return Response(ResponseSerializer(GeneralResponse(False,"You are not a member of this organisation, please wait until your membership has been approved.")).data, status=status.HTTP_400_BAD_REQUEST)
    return Response(orgserializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_emp(request):
    org_id = request.data['orgId']
    emp_id = request.data['empId']
    try:
        org_emp = OrgEmployee.objects.get(organisation__id=org_id,employee__id=emp_id)
    except Exception as e:
        return Response(ResponseSerializer(GeneralResponse(False,"Organisation not found.")).data, status=status.HTTP_400_BAD_REQUEST)
    #Check authorised
    if org_emp.organisation.owner == request.user:
        org_emp.delete()
    else:
        return Response(ResponseSerializer(GeneralResponse(False,'Sorry, you are not authorised to perform this action.')).data, status=status.HTTP_401_UNAUTHORIZED)
    orgserializer = OrganisationSerializer(org_emp.organisation,context={'user' : request.user})
    return Response(orgserializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_emp(request):
    org_id = request.data['orgId']
    emp_id = request.data['empId']
    try:
        org_emp = OrgEmployee.objects.get(organisation__id=org_id,employee__id=emp_id)
    except Exception as e:
        return Response(ResponseSerializer(GeneralResponse(False,"Organisation not found.")).data, status=status.HTTP_400_BAD_REQUEST)
    #Check authorised
    if org_emp.organisation.owner == request.user:
        org_emp.approved = True
        org_emp.save()
    else:
        return Response(ResponseSerializer(GeneralResponse(False,'Sorry, you are not authorised to perform this action.')).data, status=status.HTTP_401_UNAUTHORIZED)
    orgserializer = OrganisationSerializer(org_emp.organisation,context={'user' : request.user})
    return Response(orgserializer.data, status=status.HTTP_200_OK)
