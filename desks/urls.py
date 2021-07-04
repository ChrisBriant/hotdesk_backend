from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^createdeskmap/', views.create_desk_map, name='createdeskmap'),
]
