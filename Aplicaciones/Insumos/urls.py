from django.urls import path
from . import views


urlpatterns = [
# rutas de modulos para navegacion

    

    # Rutas de opciones insumos
    path('registrar_insumo_nuevo/', views.registrar_insumo_nuevo, name='registrar_insumo_nuevo'),
    path('ajustar_stock/<int:codigo>/', views.ajustar_stock, name='ajustar_stock'),
    path('detalle_insumo/<int:codigo>/', views.detalle_insumo, name='detalle_insumo'),
    path('insumo/eliminar/<int:insumo_id>/', views.eliminar_insumo, name='eliminar_insumo'),


]