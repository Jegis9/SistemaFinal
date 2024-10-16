from django.urls import path
from . import views


urlpatterns = [
# rutas de modulos para navegacion
    
    path('epp/', views.epp, name='epp'),
    path('estadoEPP/<int:asignado_id>/', views.estadoEPP, name='estadoEPP'),
    path('lEpp/', views.lEpp, name='lEpp'),
    path('listaEPP/', views.listaEPP, name='listaEPP'),
   path('marcar_arregladoEPP/<int:codigo>/', views.marcar_arregladoEPP, name='marcar_arregladoEPP'),

   path('epp/editar/<int:asignacion_id>/', views.editar_asignacion_epp, name='editar_asignacion_epp'),
    path('epp/eliminar/<int:asignacion_id>/', views.eliminar_asignacion_epp, name='eliminar_asignacion_epp'),
    path('editar-epp/<str:codigo_epp>/', views.editar_epp, name='editar_epp'),
    path('eliminar-epp/<str:codigo_epp>/', views.eliminar_epp, name='eliminar_epp'),
]