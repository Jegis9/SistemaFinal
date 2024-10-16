from django.shortcuts import render
from Aplicaciones.Publico.models import Emergencias
from django.shortcuts import get_object_or_404, redirect
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
from django.contrib import messages
# Create your views here.

@login_required
def EmergenciasReportadas(request):
    # Obtenemos la lista de todos los usuarios registrados
    emergencia = Emergencias.objects.filter(atendido=False)
    return render(request, 'emergenciasRecibidas.html', {"emergencia": emergencia}) 
@login_required
def emergenciasAtendidas(request):
    emergencias_atendidas = Emergencias.objects.filter(atendido=True)
    return render(request, 'emergenciasAtendidas.html', {
        
        'emergencias': emergencias_atendidas
    })
@login_required
def marcar_como_atendido(request, codigo):
    emergencia = get_object_or_404(Emergencias, codigo=codigo)
    emergencia.atendido = True
    emergencia.save()
    messages.success(request, 'Emergencia marcada como atendida.')
    return redirect('emergenciasAtendidas')  # Redirige a la lista de emergencias después de actualizar

  


def mapaPPP(request):
    return render(request,'mapa.html')