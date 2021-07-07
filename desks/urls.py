from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^createdeskmap/', views.create_desk_map, name='createdeskmap'),
	url(r'^createorg/', views.create_organisation, name='createorg'),
	url(r'^myorganisations/', views.my_orgs, name='myorganisations'),
	url(r'^joinorganisation/', views.join_org, name='joinorganisation'),
	url(r'^getorganisation/', views.get_org, name='getorganisation'),
]
