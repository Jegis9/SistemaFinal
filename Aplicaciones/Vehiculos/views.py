from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from.models import Vehiculos, Mantenimiento
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .forms import VEHForm
@login_required
def vehiculos(request):
    if request.method == 'POST':
        user = request.user  # Usuario en sesión
        placas = request.POST.get('placa')
        tipo_vehiculo = request.POST.get('tipo')

        Vehiculos.objects.create(user=user, placas=placas,  tipo_vehiculo=tipo_vehiculo)
        return redirect('vehiculos')
    
    vehiculos_list = Vehiculos.objects.filter(user=request.user)  # Mostrar solo los vehículos del usuario en sesión
    return render(request, 'vehiculos.html', {'vehiculos_list': vehiculos_list})


@login_required
def eliminar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculos, id=vehiculo_id)
    if request.method == 'POST':
        vehiculo.delete()
        return redirect('vehiculos') 
    return render(request, 'vehiculos.html')





@login_required
def mantenimientoVehiculos(request, vehiculo_id):
    vehiculo = Vehiculos.objects.get(id=vehiculo_id)  # Asegurarse que el vehículo pertenezca al usuario
    if request.method == 'POST':
        estado = request.POST.get('estado') == 'on'
        descripcion = request.POST.get('descripcion')

        Mantenimiento.objects.create(vehiculo=vehiculo, estado=estado, descripcion=descripcion)
        messages.success(request, "El vehículo ha sido reportado.")
        return redirect('vehiculos')
    

    return render(request, 'vehiculos.html')


@login_required
def lVehiculos(request):
    # Filtrar solo los vehículos que no han sido arreglados
    estados = Mantenimiento.objects.filter(estado=False)  
    return render(request, 'reportesVehiculos.html', {"estados": estados})



@login_required
def marcar_arreglado_vehiculo(request, vehiculo_id):
    estado = get_object_or_404(Mantenimiento, id=vehiculo_id)
    estado.estado = True  # Cambia el estado a "arreglado"
    estado.save()
    messages.success(request, "El vehículo ha sido marcado como arreglado.")
    return redirect('mantenimiento')  # Redirige a la lista de mantenimiento


@login_required
def editar_vehiculos(request, codigo_vehiculo):
    vehiculo = get_object_or_404(Vehiculos, id=codigo_vehiculo)
    if request.method == 'POST':
        form = VEHForm(request.POST, instance=vehiculo)
        if form.is_valid():
            form.save()
            messages.success(request, 'EPP editado correctamente.')
            return redirect('vehiculos')  # Asegúrate de que 'lista_epps' es el nombre correcto de tu vista
    else:
        form = VEHForm(instance=vehiculo)
    return render(request, 'editar_vehiculo.html', {'form': form})