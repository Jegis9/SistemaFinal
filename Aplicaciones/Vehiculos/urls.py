from django.urls import path
from . import views


urlpatterns = [
# rutas de modulos para navegacion
path('vehiculos/', views.vehiculos, name='vehiculos'),
path('mantenimientoVehiculos/<int:vehiculo_id>/', views.mantenimientoVehiculos, name='mantenimientoVehiculos'),
path('vehiculo/eliminar/<int:vehiculo_id>/', views.eliminar_vehiculo, name='eliminar_vehiculo'),
path('marcar_arreglado_vehiculo/<int:vehiculo_id>', views.marcar_arreglado_vehiculo, name='marcar_arreglado_vehiculo'),
path('editar-vehiculo/<str:codigo_vehiculo>/', views.editar_vehiculos, name='editar_vehiculo'),
path('mantenimiento/', views.lVehiculos, name='mantenimiento'),


]

