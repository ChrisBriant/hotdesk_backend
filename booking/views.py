from django.contrib.auth import authenticate
from django.db import IntegrityError
from django.http import JsonResponse
from rest_framework.decorators import api_view,authentication_classes,permission_classes,action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from .models import *
from hotdesk.serializers import *
import random, string, pytz
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_booking(request):
    desk_id = request.data['deskId']
    try:
        desk = Desk.objects.get(id=desk_id)
    except Exception as e:
        return Response(ResponseSerializer(GeneralResponse(False,"Desk does not exist.")).data, status=status.HTTP_400_BAD_REQUEST)
    date_str = request.data['date']
    booking_date = datetime.strptime(date_str, "%d/%m/%Y")
    #Check authorised to book
    if desk.plan.floor.building.organisation.orgemployee_set.all()\
        .filter(employee=request.user).count() > 0:
        try:
            booking = Booking.objects.create(
                desk=desk,
                user=request.user,
                date=booking_date
            )
        except Exception as e:
            return Response(ResponseSerializer(GeneralResponse(False,"Booking failed.")).data, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(ResponseSerializer(GeneralResponse(False,"Unauthorised to make this booking.")).data, status=status.HTTP_403_FORBIDDEN)
    serializer = BookingSerializer(booking)
    return Response(serializer.data,status=status.HTTP_201_CREATED)

def create_slots(start,end):
    slots = []
    delta = timedelta(days=1)
    while start != end:
        slot = dict()
        slot['date'] = pytz.utc.localize(start)
        start = start + delta
        slots.append(slot)
    return slots


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_bookings(request):
    org_id = request.data['orgId']
    floor_id = request.data['floorId']
    desk_count = Desk.objects.filter(plan__floor__id=floor_id).count()
    try:
        org = Organisation.objects.get(id=org_id)
    except Exception as e:
        return Response(ResponseSerializer(GeneralResponse(False,"Organisation does not exist.")).data, status=status.HTTP_400_BAD_REQUEST)
    #Check authorised
    if org.orgemployee_set.all().filter(employee=request.user).count() > 0:
        #Store the booking data
        booking_data = dict()
        booking_data['desk_count'] = desk_count
        #Get time range
        month = request.data['month']
        year = request.data['year']
        date_from = datetime(day=1,month=int(month),year=int(year))
        date_to = date_from +  relativedelta(months=1)
        slots = create_slots(date_from,date_to)
        #Get the bookings
        #Change from date to current if in future
        format = "%Y-%m-%d"
        monthly_bookings = Booking.objects.filter(\
                date__range=[date_from.strftime(format), date_to.strftime(format)],\
                desk__plan__floor__id=floor_id\
                ).order_by('date')
        out_slots = dict()
        for slot in slots:
            date_str = slot['date'].strftime('%d/%m/%Y')
            out_slots[date_str] = []
            daily_bookings = monthly_bookings.filter(date=slot['date'])
            for bk in daily_bookings:
                desk_obj = dict()
                desk_obj['name'] = bk.desk.name
                desk_obj['id'] = bk.desk.id
                out_slots[date_str].append(desk_obj)
        booking_data['out_slots'] = out_slots
    else:
        return Response(ResponseSerializer(GeneralResponse(False,"Unauthorised to make this booking.")).data, status=status.HTTP_403_FORBIDDEN)
    return JsonResponse(booking_data,safe=False)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def my_bookings(request):
    org_id = request.data.get('orgId')
    yesterday = datetime.now() + timedelta(days=-1)
    #Get bookings by organisation if org_id is present
    if org_id:
        bookings = Booking.objects.filter(user=request.user,date__gte=yesterday,
            desk__plan__floor__building__organisation__id=org_id)\
            .order_by('date')
    else:
        bookings = Booking.objects.filter(user=request.user,date__gte=yesterday).order_by('date')
    serializer = BookingSerializer(bookings,many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def org_bookings(request):
    org_id = request.data.get('orgId')
    #Check authorised
    try:
        org = Organisation.objects.get(id=org_id)
    except Exception as e:
        return Response(ResponseSerializer(GeneralResponse(False,"Organisation does not exist.")).data, status=status.HTTP_400_BAD_REQUEST)
    if org.owner != request.user:
        return Response(ResponseSerializer(GeneralResponse(False,"You are not authorised to access this organisations bookings.")).data, status=status.HTTP_403_FORBIDDEN)
    yesterday = datetime.now() + timedelta(days=-1)
    bookings = Booking.objects.filter(date__gte=yesterday,
        desk__plan__floor__building__organisation=org)\
        .order_by('date')
    serializer = BookingSerializer(bookings,many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['DELETE','OPTIONS'])
@permission_classes([IsAuthenticated])
def delete_booking(request):
    org_id = request.data['orgId']
    try:
        org = Organisation.objects.get(id=org_id)
    except Exception as e:
        return Response(ResponseSerializer(GeneralResponse(False,"Organisation does not exist.")).data, status=status.HTTP_400_BAD_REQUEST)
    booking_id = request.data['bookingId']
    try:
        booking = Booking.objects.get(id=booking_id,
            desk__plan__floor__building__organisation__id=org_id)
    except Exception as e:
        return Response(status=status.HTTP_204_NO_CONTENT)
    #Check authorised
    if (booking.user == request.user) or (org.owner == request.user):
        booking.delete()
        #Return booking listings
        yesterday = datetime.now() + timedelta(days=-1)
        bookings = Booking.objects.filter(user=request.user,date__gte=yesterday,
            desk__plan__floor__building__organisation=org)\
            .order_by('date')
        serializer=BookingSerializer(bookings,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)
