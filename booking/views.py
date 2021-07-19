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
        print("Date Range", date_from,date_to)
        slots = create_slots(date_from,date_to)
        #Get the bookings
        #Change from date to current if in future
        # if not date_from > datetime.now():
        #     date_from =datetime.now()
        format = "%Y-%m-%d"
        monthly_bookings = Booking.objects.filter(\
                date__range=[date_from.strftime(format), date_to.strftime(format)],\
                desk__plan__floor__id=floor_id\
                ).order_by('date')
        for booking in monthly_bookings:
            print('BOOKING',booking.date)
        out_slots = dict()
        for slot in slots:
            print('slot',slot['date'])
            #out_slot = dict()
            date_str = slot['date'].strftime('%d/%m/%Y')
            out_slots[date_str] = []
            daily_bookings = monthly_bookings.filter(date=slot['date'])
            for bk in daily_bookings:
                desk_obj = dict()
                desk_obj['name'] = bk.desk.name
                desk_obj['id'] = bk.desk.id
                out_slots[date_str].append(desk_obj)
                print(bk.desk.name)
            #out_slots.append(out_slot)
        booking_data['out_slots'] = out_slots
        #print(out_slots)
    else:
        return Response(ResponseSerializer(GeneralResponse(False,"Unauthorised to make this booking.")).data, status=status.HTTP_403_FORBIDDEN)
    return JsonResponse(booking_data,safe=False)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user,date__gte=datetime.now())
    serializer = BookingSerializer(bookings,many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
