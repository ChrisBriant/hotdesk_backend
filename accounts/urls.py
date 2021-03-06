from django.conf.urls import url
from . import apiviews

urlpatterns = [
	#Authenticate to be taken out after testing /autneticate which has the custom claims
	url(r'^authenticate/',apiviews.get_token, name='authenticate'),
	url(r'^register/$', apiviews.register, name='register'),
	url(r'^forgotpassword/$', apiviews.forgot_password, name='forgotpassword'),
	url(r'^changepassword/$', apiviews.change_password, name='changepassword'),
]
