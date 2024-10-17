# Estadisticas/views.py
from django.shortcuts import render
from Aplicaciones.Publico.models import Emergencias
from django.contrib.auth.models import User
from Aplicaciones.Herramientas.models import EstadoHerramienta,Herramienta
from Aplicaciones.Insumos.models import Insumo
from Aplicaciones.EPP.models import EstadoEPP,Epp
from Aplicaciones.Vehiculos.models import Vehiculos
from Aplicaciones.CV.models import CV
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied

from Aplicaciones.user.models import Profile

# Funciones auxiliares para verificar permisos
def is_admin(user):
    return user.groups.filter(name='Administrador').exists()

def is_staff(user):
    return user.groups.filter(name='Personal').exists()
def is_admin_or_staff(user):
    return user.is_authenticated and user.groups.filter(name__in=['Administrador', 'Personal']).exists()



@login_required


def estadisticas(request):
    # Contadores para emergencias
    total_emergencias_atendidas = Emergencias.objects.filter(atendido=True).count()
    total_emergencias_pendientes = Emergencias.objects.filter(atendido=False).count()
    
    # Contadores para usuarios
    total_usuarios_internos = User.objects.filter(profile__is_internal=True).count()
    total_usuarios_externos = User.objects.filter(profile__is_internal=False).count()
    total_cv = CV.objects.count()
    
    # Contadores para herramientas
    total_herramientas_malas = EstadoHerramienta.objects.filter(estado__in=["malo", "Malo"]).count()
    total_herramientas_arregladas = EstadoHerramienta.objects.filter(estado__in=["Bueno", "arreglado"]).count()
    total_herramientas = Herramienta.objects.count()
    emergencias_pendientes = Emergencias.objects.filter(atendido=False).count()
    
    total_insumos = Insumo.objects.count()
    # Contar insumos con stock alto (mayor o igual a 50)
    total_insumos_alto = Insumo.objects.filter(stock_actual__gte=50).count()

    # Contar insumos con stock medio (menor o igual a 25)
    total_insumos_medio = Insumo.objects.filter(stock_actual__lte=50).count()

    # Contar insumos con stock bajo (menor o igual a 10)
    total_insumos_bajo = Insumo.objects.filter(stock_actual__lte=10).count()

    
    
    total_reportes_epp = EstadoEPP.objects.filter(estado='Malo').count()
    total_epp = Epp.objects.count()
    tatal_vehiculos = Vehiculos.objects.count()
    
    context = {
        'emergencias_atendidas': total_emergencias_atendidas,
        'emergencias_pendientes': total_emergencias_pendientes,
        'usuarios_internos': total_usuarios_internos,
        'usuarios_externos': total_usuarios_externos,
        'herramientas_malas': total_herramientas_malas,
        'total_herramientas': total_herramientas,
        'herramientas_arregladas': total_herramientas_arregladas,
        'emergencias_pendientes': emergencias_pendientes,
        'total_insumos':total_insumos,
        'total_insumos_alto':total_insumos_alto,
        'total_insumos_medio':total_insumos_medio,
        'total_insumos_bajo':total_insumos_bajo,
        'total_reportes_epp':total_reportes_epp,
        'total_epp':total_epp,
        'tatal_vehiculos':tatal_vehiculos,
        'total_cv':total_cv
    }
    
    return render(request, 'estadisticas.html', context) 