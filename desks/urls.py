from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^createdeskmap/', views.create_desk_map, name='createdeskmap'),
	url(r'^createorg/', views.create_organisation, name='createorg'),
	url(r'^myorganisations/', views.my_orgs, name='myorganisations'),
	url(r'^joinorganisation/', views.join_org, name='joinorganisation'),
	url(r'^getorganisation/', views.get_org, name='getorganisation'),
	url(r'^reject/', views.reject_emp, name='reject'),
	url(r'^accept/', views.accept_emp, name='accept'),
	url(r'^addbuilding/', views.add_building, name='addbuilding'),
	url(r'^addfloor/', views.add_floor, name='addfloor'),
	url(r'^addplan/', views.add_plan, name='addplan'),
	url(r'^adddeskplan/', views.add_desk_plan, name='adddeskplan'),
]
