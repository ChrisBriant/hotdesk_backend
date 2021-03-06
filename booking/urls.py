from django.conf.urls import url
from . import views

urlpatterns = [
	#Authenticate to be taken out after testing /autneticate which has the custom claims
	url(r'^makebooking/',views.make_booking, name='makebooking'),
    url(r'^getbookings/',views.get_bookings, name='getbookings'),
    url(r'^mybookings/',views.my_bookings, name='mybookings'),
	url(r'^cancelbooking/',views.delete_booking, name='cancelbooking'),
	url(r'^bookingsfororg/',views.org_bookings, name='bookingsfororg'),
]
