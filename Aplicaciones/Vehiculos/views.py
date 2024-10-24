from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from.models import Vehiculos, Mantenimiento
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .forms import VEHForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.utils import timezone
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
def vehiculos(request):
    if request.method == 'POST':
        user = request.user  # Usuario en sesión
        placas = request.POST.get('placa')
        tipo_vehiculo = request.POST.get('tipo')

        Vehiculos.objects.create(user=user, placas=placas,  tipo_vehiculo=tipo_vehiculo)
        return redirect('vehiculos')
    
    vehiculos_list = Vehiculos.objects.all()  # Mostrar solo los vehículos del usuario en sesión
    return render(request, 'vehiculos.html', {'vehiculos_list': vehiculos_list})


@login_required
@user_passes_test(is_admin, login_url='error')
def eliminar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculos, id=vehiculo_id)
    if request.method == 'POST':
        vehiculo.delete()
        return redirect('vehiculos') 
    return render(request, 'vehiculos.html')




@login_required
@user_passes_test(is_admin_or_staff, login_url='error')
def mantenimientoVehiculos(request, vehiculo_id):
    vehiculo = Vehiculos.objects.get(id=vehiculo_id)  # Asegurarse que el vehículo pertenezca al usuario
    if request.method == 'POST':
        estado = request.POST.get('estado') == 'on'
        descripcion = request.POST.get('descripcion')

        Mantenimiento.objects.create(vehiculo=vehiculo, estado=estado, descripcion=descripcion)
        # Preparar los datos para enviar por correo
        nombre_persona = request.user.get_full_name() or request.user.username
        nombre_vehiculo = vehiculo.nombre  # Nombre del vehículo
        fecha_reportado = timezone.now()

        # Crear el mensaje del correo
        mensaje_correo = (
            f"Nuevo Reporte de Mantenimiento de Vehículo\n\n"
            f"Persona: {nombre_persona}\n"
            f"Vehículo: {nombre_vehiculo}\n"
            f"Estado: {'Operativo' if estado else 'Fuera de servicio'}\n"
            f"Descripción: {descripcion}\n"
            f"Fecha Reportado: {fecha_reportado}\n"
        )

        # Enviar el correo
        send_mail(
            subject='Nuevo Reporte de Mantenimiento de Vehículo',
            message=mensaje_correo,
                from_email='bomberosmunicipalestotonicapan@gmail.com',  # Cambia por el correo al que quieres enviar
                recipient_list=['forniteb6@gmail.com'],
            fail_silently=False,
        )
        
        messages.success(request, "El vehículo ha sido reportado.")
        return redirect('vehiculos')
    

    return render(request, 'vehiculos.html')


@login_required
@user_passes_test(is_admin, login_url='error')
def lVehiculos(request):
    # Filtrar solo los vehículos que no han sido arreglados
    estados = Mantenimiento.objects.filter(estado=False)  
    return render(request, 'reportesVehiculos.html', {"estados": estados})



@login_required
@user_passes_test(is_admin, login_url='error')
def marcar_arreglado_vehiculo(request, vehiculo_id):
    estado = get_object_or_404(Mantenimiento, id=vehiculo_id)
    estado.estado = True  # Cambia el estado a "arreglado"
    estado.save()
    messages.success(request, "El vehículo ha sido marcado como arreglado.")
    return redirect('mantenimiento')  # Redirige a la lista de mantenimiento


@login_required
@user_passes_test(is_admin, login_url='error')
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