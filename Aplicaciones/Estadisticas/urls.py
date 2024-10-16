from django.urls import path
from . import views


urlpatterns = [
# rutas de modulos para navegacion
    
    path('estadisticas/', views.estadisticas, name='estadisticas'),
 


  
]