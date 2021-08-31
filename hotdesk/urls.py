from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from accounts import views as account_views
#For media
from django.conf.urls.static import static
from django.conf import settings
#Custom claims in token
from .customtoken import CustomTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account/', include('accounts.urls')),
    path('api/desks/', include('desks.urls')),
    path('api/booking/', include('booking.urls')),
    url(r'confirm/(?P<hash>\w+)/',account_views.confirm,name='confirm'),
    url(r'passwordreset/(?P<hash>\w+)/',account_views.passreset_api,name='passwordreset'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
