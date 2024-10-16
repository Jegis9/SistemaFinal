from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('reportEmergency/', views.reportEmergency, name='reportEmergency'),
    path('reportarEmergencia/', views.reportarEmergencia, name='reportarEmergencia'),
    path('profile/', views.profile, name='profile' ), # ruta para llamar a la vista profile o perfil z
  
    path('profile_Interno', views.profile_Interno, name='profile_Interno')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 


