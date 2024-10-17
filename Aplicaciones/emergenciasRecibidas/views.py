from django.shortcuts import render
from Aplicaciones.Publico.models import Emergencias
from django.shortcuts import get_object_or_404, redirect
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
from django.contrib import messages
# Create your views here.
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
@user_passes_test(is_admin_or_staff, login_url='error')
def EmergenciasReportadas(request):
    # Obtenemos la lista de todos los usuarios registrados
    emergencia = Emergencias.objects.filter(atendido=False)
    return render(request, 'emergenciasRecibidas.html', {"emergencia": emergencia}) 



@login_required
@user_passes_test(is_admin_or_staff, login_url='error')
def emergenciasAtendidas(request):
    emergencias_atendidas = Emergencias.objects.filter(atendido=True)
    return render(request, 'emergenciasAtendidas.html', {
        
        'emergencias': emergencias_atendidas
    })
    
    
    
@login_required
@user_passes_test(is_admin_or_staff, login_url='error')
def marcar_como_atendido(request, codigo):
    emergencia = get_object_or_404(Emergencias, codigo=codigo)
    emergencia.atendido = True
    emergencia.save()
    messages.success(request, 'Emergencia marcada como atendida.')
    return redirect('emergenciasAtendidas')  # Redirige a la lista de emergencias después de actualizar

  


def mapaPPP(request):
    return render(request,'mapa.html')