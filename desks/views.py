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
    orgserializer = OrganisationSerializer(org,context={'user' : request.user})
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
    return Response(ResponseSerializer(GeneralResponse(True,"Succesfully joined {} please await approval.".format(org.name))).data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_org(request):
    org_id = request.data['orgId']
    print("here",org_id)
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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_building(request):
    org_id = request.data['orgId']
    name = request.data['name']
    try:
        org = Organisation.objects.get(id=org_id)
    except Exception as e:
        print(e)
        return Response(ResponseSerializer(GeneralResponse(False,"Organisation not found.")).data, status=status.HTTP_400_BAD_REQUEST)
    if org.owner == request.user:
        building = Building.objects.create(
            name=name,
            organisation=org
        )
    orgserializer = OrganisationSerializer(org,context={'user':request.user})
    return Response(orgserializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_floor(request):
    build_id = request.data['buildingId']
    name = request.data['name']
    level = request.data['level']
    try:
        building = Building.objects.get(id=build_id)
    except Exception as e:
        print(e)
        return Response(ResponseSerializer(GeneralResponse(False,"Organisation not found.")).data, status=status.HTTP_400_BAD_REQUEST)
    if building.organisation.owner == request.user:
        floor = Floor.objects.create(
            name=name,
            level=level,
            building=building
        )
    orgserializer = OrganisationSerializer(building.organisation,context={'user':request.user})
    return Response(orgserializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_plan(request):
    floor_id=request.data['floorId']
    try:
        floor = Floor.objects.get(id=floor_id)
    except Exception as e:
        print(e)
        return Response(ResponseSerializer(GeneralResponse(False,"Floor not found.")).data, status=status.HTTP_400_BAD_REQUEST)
    if floor.building.organisation.owner == request.user:
        print('FILES',request.FILES)
        if request.FILES['picture']:
            #First try to get existing plan
            try:
                #We want to overwrite the plan if it exists
                plan = Plan.objects.get(floor=floor)
                plan.picture = request.FILES['picture']
                try:
                    plan.full_clean()
                    plan.save()
                except Exception as e:
                    print(e)
                    return Response(ResponseSerializer(GeneralResponse(False,"Unable to upload image")).data, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                #Plan doesn't exist create new one
                plan = Plan(
                    floor=floor,
                    picture=request.FILES['picture'],
                    creator=request.user
                )
                try:
                    plan.full_clean()
                    plan.save()
                except Exception as e:
                    print(e)
                    return Response(ResponseSerializer(GeneralResponse(False,"Unable to upload image")).data, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(ResponseSerializer(GeneralResponse(False,"You are not authorised to upload to this organisation.")).data, status=status.HTTP_401_UNAUTHORIZED)
    serializer = PlanSerializer(plan)
    return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_desk_plan(request):
    plan_id = request.data['planId'];
    try:
        plan = Plan.objects.get(id=plan_id)
    except Exception as e:
        return Response(ResponseSerializer(GeneralResponse(False,"Plan does not exist.")).data, status=status.HTTP_400_BAD_REQUEST)
    #Delete all the existing desks
    plan.desk_set.all().delete()
    for desk in request.data['desks']:
        new_desk = Desk.objects.create(
            plan = plan,
            desk_id = desk['deskId'],
            name =  desk['name'],
            x = desk['x'],
            y = desk['y'],
            w = desk['w'],
            h = desk['h']
        )
    serializer =  PlanSerializer(plan)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
