from django.urls import path
from . import views


urlpatterns = [
# rutas de modulos para navegacion
    path('home/', views.home, name='home'),

    # path('insumos/', views.insumos, name='insumos'),


    
    
    
    # rutas de opciones insumos
    path('registrarInsumo/', views.registrarInsumo),
    path('edicionInsumo/<codigo>', views.edicionInsumo),
    path('editarInsumo/', views.editarInsumo),
    path('eliminacionInsumo/<codigo>', views.eliminacionInsumo),
    path('eliminacionInsumo/<codigo>', views.eliminacionInsumo),
    
    path('errores/', views.errores, name='errores')
]