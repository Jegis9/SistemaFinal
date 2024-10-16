from django.urls import path
from . import views


urlpatterns = [
# rutas de modulos para navegacion
    path('desactivar_usuario/<int:user_id>/', views.desactivar_usuario, name='desactivar_usuario'),
    path('activar_usuario/<int:user_id>/', views.activar_usuario, name='activar_usuario'),

path('desactivar_usuario_publico/<int:user_id>/', views.desactivar_usuario_publico, name='desactivar_usuario_publico'),
path('activar_usuario_publico/<int:user_id>/', views.activar_usuario_publico, name='activar_usuario_publico'),


    path('lUsuarios/', views.lUsuarios, name='lUsuarios'),
    path('lInternos', views.lInternos, name='lInternos'),
    
  
]

