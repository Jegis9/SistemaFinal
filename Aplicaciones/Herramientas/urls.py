from django.urls import path
from . import views


urlpatterns = [
# rutas de modulos para navegacion
    
    path('herramientas/', views.herramienta, name='herramientas'),
    path('estadoHerramienta/<int:herramienta_id>/', views.estadoHerramienta, name='estadoHerramienta'),
    path('lEHerramientas/', views.lEHerramientas, name='lEHerramientas'),
    path('marcar_arreglado/<int:codigo>', views.marcar_arreglado, name='marcar_arreglado'),

    path('herramienta/eliminar/<int:herramienta_id>/', views.eliminar_herramienta, name='eliminar_herramienta'),
  path('listaHerramienta/', views.listaHerramientas, name='listaHerramienta'),
       path('editar-herramienta/<str:codigo_her>/', views.editar_Herramientas, name='editar_herramienta'),
       path('editar-mantenimiento/<int:codigo_mant>/', views.editar_Mantenimeinto, name='editar_mantenimiento'),
    path('eliminar-herramienta/<str:codigo_her>/', views.eliminar_Herramientas, name='eliminar_herramientas'),
 
]