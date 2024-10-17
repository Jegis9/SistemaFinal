"""
URL configuration for Sistema project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views #importacion de librerias para login y logout de cada usuario en cada una de sus vistas

from django.conf.urls import handler404, handler500
from Aplicaciones.Administrativo.views import errores

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Aplicaciones.Administrativo.urls')),
    path('', include('Aplicaciones.user.urls')),
    path('', include('Aplicaciones.Publico.urls')),
    path('', include('Aplicaciones.emergenciasRecibidas.urls')),
    path('', include('Aplicaciones.lUsuarios.urls')),
    path('', include('Aplicaciones.Personal.urls')),
    path('', include('Aplicaciones.Vehiculos.urls')),
    path('', include('Aplicaciones.EPP.urls')),
    path('', include('Aplicaciones.Herramientas.urls')),
    path('', include('Aplicaciones.Estadisticas.urls')),
    path('', include('Aplicaciones.Insumos.urls')),
    path('', include('Aplicaciones.Emergencias.urls')),
    path('', include('Aplicaciones.CV.urls')),
    
    
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout')
 
    
]
handler404 = errores

# Registrar el manejo de errores
handler500 = errores