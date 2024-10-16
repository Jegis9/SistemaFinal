from django.urls import path
from . import views


urlpatterns = [
# rutas de modulos para navegacion
    
    path('EmergenciasReportadas/', views.EmergenciasReportadas, name='EmergenciasReportadas'),
    path('marcar_como_atendido/<int:codigo>/', views.marcar_como_atendido, name='marcar_como_atendido'),
    path('emergenciasAtendidas/', views.emergenciasAtendidas, name='emergenciasAtendidas'),
    path('mapa/', views.mapaPPP, name='mapa')
    
    
]