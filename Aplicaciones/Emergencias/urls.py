from django.urls import path
from . import views

urlpatterns = [
    path('add/',views.servicio_create_view, name='add'),
    path('lista_servicios/', views.servicio_list_view, name='lista_servicios'),
    path('prueba_catr/', views.prueba_catr, name='prueba_catr'),
    
    path('varios/', views.varios_list_view, name='varios'),
    path('ambulancia/', views.ambulancia_list_view, name='ambulancia'),
    path('incendios/', views.incendios_list_view, name='incendios'),
    path('ambulancia/<int:ambulancia_id>/reporte/', views.generar_reporte_ambulancia, name='generar_reporte_ambulancia'),
    path('varios/<int:varios_id>/reporte/', views.generar_reporte_servicios_varios, name='generar_reporte_varios'),
    path('incendios/<int:incendio_id>/reporte/', views.generar_reporte_incendios, name='generar_reporte_incendios'),
    path('editar_desactivar_varios/<int:pk>/', views.editar_desactivar_varios, name='editar_desactivar_varios'),
    path('pruebaservicios/', views.tabla_servicios, name='pruebaservicios'),
    path('vista_kilometraje/', views.vista_kilometraje, name='vista_kilometraje'),
    path('reporte_ambulancia/', views.reporte_ambulancia, name='reporte_ambulancia'),
    path('eliminar_servicio_varios/<int:servicio_id>/', views.eliminar_servicio_vario, name='eliminar_servicio_varios'),
    path('editar_servicio_varios/<int:servicio_id>/<int:vario_id>/', views.editar_servicio_vario, name='editar_servicio_varios'),
    path('eliminar_servicio_ambulancia/<int:servicio_id>/', views.eliminar_servicio_ambulancia, name='eliminar_servicio_ambulancia'),
    path('editar_servicio_ambulancia/<int:servicio_id>/<int:ambulancia_id>/', views.editar_servicio_ambulancia, name='editar_servicio_ambulancia'),
    path('eliminar_servicio_incendios/<int:servicio_id>/', views.eliminar_servicio_incendios, name='eliminar_servicio_incendios'),
    path('editar_servicio_incendios/<int:servicio_id>/<int:incendio_id>/', views.editar_servicio_incendios, name='editar_servicio_incendios'),
    
    path('crear/', views.crear_categoria, name='crear_categoria'),

  
]
