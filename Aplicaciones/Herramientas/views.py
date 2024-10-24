from django.shortcuts import render

# Create your views here.

from django.core.mail import send_mail

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Herramienta, EstadoHerramienta, MantenimientoHerramienta
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import HerramientasForm,MantenimientoForm
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
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
def herramienta(request):
    if request.method == 'POST':
        herramienta_id = request.POST.get('herramienta')
        descripcion = request.POST.get('descripcion')
        tiempo_mantenimiento = request.POST.get('tiempo_mantenimiento')

        if herramienta_id and descripcion and tiempo_mantenimiento:
            herramienta = Herramienta.objects.get(codigo=herramienta_id)
            MantenimientoHerramienta.objects.create(
                herramienta=herramienta,
                descripcion=descripcion,
                tiempo_mantenimiento=tiempo_mantenimiento
            )
            
                        # Enviar correo con la información del mantenimiento
            send_mail(
                subject='Nuevo mantenimiento registrado',
                message=f'Se ha registrado un nuevo mantenimiento para la herramienta {herramienta.nombre}. Descripción: {descripcion}. Fecha de mantenimiento: {tiempo_mantenimiento}.',
                from_email='bomberosmunicipalestotonicapan@gmail.com',  # Asegúrate de que coincida con tu configuración
                recipient_list=['forniteb6@gmail.com'],  # Reemplaza con la dirección de correo del destinatario
                fail_silently=False,
            )

        # Si se quiere agregar una nueva herramienta
        nuevo_herramienta = request.POST.get('nuevo_herramienta')
        if nuevo_herramienta:
            Herramienta.objects.create(nombre=nuevo_herramienta)

        return redirect('herramientas')

    else:
        herramientas = Herramienta.objects.all()
        mantenimientos = MantenimientoHerramienta.objects.all()
        return render(request, 'herramientasS.html', {
            "herramientas": herramientas,
            "mantenimientos": mantenimientos,
        })



@login_required
@user_passes_test(is_admin, login_url='error')

def eliminar_herramienta(request, herramienta_id):
    herramienta = get_object_or_404(MantenimientoHerramienta, codigo=herramienta_id)
    if request.method == 'POST':
        herramienta.delete()
        return redirect('herramientas') 
    return render(request, 'herramientasS.html')



@login_required
@user_passes_test(is_admin_or_staff, login_url='error')
def estadoHerramienta(request, herramienta_id):
    if request.method == 'POST':
        descripcion = request.POST.get('descripcion')
        estado = request.POST.get('estado')
        
        herramienta = Herramienta.objects.get(codigo=herramienta_id)  # Asegúrate de que 'asignado_id' sea un id correcto

        if descripcion and estado:
            EstadoHerramienta.objects.create(
                herramienta=herramienta,
                descripcion=descripcion,
                estado=estado
            )
                    # Enviar correo con la información del estado de la herramienta
            send_mail(
                subject='Actualización del estado de herramienta',
                message=f'El estado de la herramienta {herramienta.nombre} ha sido actualizado. Descripción: {descripcion}. Estado: {estado}.',
                from_email='bomberosmunicipalestotonicapan@gmail.com',  # Asegúrate de que coincida con tu configuración
                recipient_list=['forniteb6@gmail.com'],  # Reemplaza con la dirección de correo del destinatario
                fail_silently=False,
            )


        return redirect('lEHerramientas')
    else:
        return render(request, 'herramientasEstado.html')



@login_required
@user_passes_test(is_admin, login_url='error')
def marcar_arreglado(request, codigo):
    estado = get_object_or_404(EstadoHerramienta, codigo=codigo)
    estado.estado = "Bueno"  # Cambia el estado a "arreglado"
    estado.save()
    messages.success(request, "La herramienta ha sido marcada como arreglada.")
    return redirect('lEHerramientas')  # Redirige de nuevo a la lista


@login_required
@user_passes_test(is_admin_or_staff, login_url='error')

def lEHerramientas(request):
    estados = EstadoHerramienta.objects.filter(estado__in=["malo", "Malo"])  # Filtrar solo los estados no arreglados
    return render(request, 'lHerramientas.html', {"estados": estados})



 
@login_required
@user_passes_test(is_admin, login_url='error')
def listaHerramientas(request):

    her = Herramienta.objects.all()
    return render(request, 'listaHerramienta.html', {"her": her})


@login_required
@user_passes_test(is_admin, login_url='error')
def eliminar_Herramientas(request, codigo_her):
    her = get_object_or_404(Herramienta, codigo=codigo_her)
    if request.method == 'POST':
        her.delete()
        messages.success(request, 'Herramienta eliminado correctamente.')
        return redirect('listaHerramienta')  # Asegúrate de que 'lista_epps' es el nombre correcto de tu vista
    return render(request, 'listaHerramienta.html', {'her': her})



@login_required
@user_passes_test(is_admin, login_url='error')
def editar_Herramientas(request, codigo_her):
    her = get_object_or_404(Herramienta, codigo=codigo_her)
    if request.method == 'POST':
        form = HerramientasForm(request.POST, instance=her)
        if form.is_valid():
            form.save()
            messages.success(request, 'Herramienta editada correctamente.')
            return redirect('listaHerramienta')  # Asegúrate de que 'lista_epps' es el nombre correcto de tu vista
    else:
        form = HerramientasForm(instance=her)
    return render(request, 'editar_herramienta.html', {'form': form})



@login_required
@user_passes_test(is_admin_or_staff, login_url='error')
def editar_Mantenimeinto(request, codigo_mant):
    mant = get_object_or_404(MantenimientoHerramienta, codigo=codigo_mant)
    if request.method == 'POST':
        form = MantenimientoForm(request.POST, instance=mant)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mantenimiento editado correctamente.')
            return redirect('herramientas')  
    else:
        form = MantenimientoForm(instance=mant)
    return render(request, 'editar_mantenimiento.html', {'form': form})





