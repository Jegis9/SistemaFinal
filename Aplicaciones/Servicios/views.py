# your_app/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ServicioForm
from .models import ServicioPrincipal

# def agregar_servicio(request):
#     if request.method == 'POST':
#         form = ServicioForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Servicio registrado exitosamente.')
#             return redirect('agregar_servicio')
#         else:
#             messages.error(request, 'Hubo un error al registrar el servicio.')
#     else:
#         form = ServicioForm()
#     return render(request, 'agregar_servicio.html', {'form': form})


# def lista_varios(request):
#     servicios_varios = ServicioPrincipal.objects.filter(servicio='Varios')
#     return render(request, 'servicios_varios.html', {'servicios_varios': servicios_varios})

# def lista_ambulancia(request):
#     servicios_ambulancia = ServicioPrincipal.objects.filter(servicio='Ambulancia')
#     return render(request, 'servicios_ambulancia.html', {'servicios_ambulancia': servicios_ambulancia})

# def lista_incendios(request):
#     servicios_incendios = ServicioPrincipal.objects.filter(servicio='Incendios')
#     return render(request, 'servicios_incendios.html', {'servicios_incendios': servicios_incendios})