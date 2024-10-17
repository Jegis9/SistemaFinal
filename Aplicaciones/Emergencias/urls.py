from django.urls import path
from . import views

urlpatterns = [
    path('add/',views.servicio_create_view, name='add'),
    path('lista_servicios/', views.servicio_list_view, name='lista_servicios'),
    path('varios/', views.varios_list_view, name='varios'),
    path('ambulancia/', views.ambulancia_list_view, name='ambulancia'),
    path('incendios/', views.incendios_list_view, name='incendios'),
    path('ambulancia/<int:ambulancia_id>/reporte/', views.generar_reporte_ambulancia, name='generar_reporte_ambulancia'),
    path('varios/<int:varios_id>/reporte/', views.generar_reporte_servicios_varios, name='generar_reporte_varios'),
    path('incendios/<int:incendio_id>/reporte/', views.generar_reporte_incendios, name='generar_reporte_incendios'),
    path('editar_desactivar_varios/<int:pk>/', views.editar_desactivar_varios, name='editar_desactivar_varios'),
    path('pruebaservicios/', views.tabla_servicios, name='pruebaservicios'),
    path('vista_kilometraje/', views.vista_kilometraje, name='vista_kilometraje'),
    path('reporte_ambulancia/', views.reporte_ambulancia, name='reporte_ambulancia')
    # path('servicios/', views.lista_servicios, name='lista_servicios'),  # Nueva URL
    # path('servicios/varios/', views.lista_varios, name='lista_varios'),
    # path('servicios/ambulancia/', views.lista_ambulancia, name='lista_ambulancia'),
    # path('servicios/incendios/', views.lista_incendios, name='lista_incendios'),
]
