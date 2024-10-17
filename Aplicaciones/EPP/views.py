from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Epp, PersonalEpps, EstadoEPP
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import AsignacionEppForm, EPPForm
from django.core.mail import send_mail
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

def epp(request):
    if request.method == 'POST':
        personal_id = request.POST.get('personal')
        epp_id = request.POST.get('epp')

        if personal_id and epp_id:
            # Obtén las instancias de User y Epp para guardarlas en el modelo de relación
            personal = User.objects.get(id=personal_id)
            epp = Epp.objects.get(codigo=epp_id)

            # Crear la asignación de EPP al personal
            PersonalEpps.objects.create(idPersonal=personal, idEpp=epp)

        # Si se quiere agregar un nuevo EPP
        nuevo_epp = request.POST.get('nuevo_epp')
        if nuevo_epp:
            Epp.objects.create(nombre=nuevo_epp)

        return redirect('epp')  # Redireccionar después de guardar

    else:
        users = User.objects.filter(profile__is_internal=True)
        epps = Epp.objects.all()
        asignaciones = PersonalEpps.objects.all()
        return render(request, 'epp.html', {
            "users": users, 
            "epps": epps, 
            "asignaciones": asignaciones
        })
        
@login_required
@user_passes_test(is_admin, login_url='error')
def editar_asignacion_epp(request, asignacion_id):
    asignacion = get_object_or_404(PersonalEpps, id=asignacion_id)
    if request.method == 'POST':
        form = AsignacionEppForm(request.POST, instance=asignacion)
        if form.is_valid():
            form.save()
            return redirect('epp')  # O a donde desees redirigir
    else:
        form = AsignacionEppForm(instance=asignacion)
    return render(request, 'editar_asignacion_epp.html', {'form': form, 'asignacion': asignacion})


@login_required
@user_passes_test(is_admin, login_url='error')
def eliminar_asignacion_epp(request, asignacion_id):
    asignacion = get_object_or_404(PersonalEpps, id=asignacion_id)
    if request.method == 'POST':
        asignacion.delete()
        return redirect('epp')  # O a donde desees redirigir
    return render(request, 'confirmar_eliminar_asignacion_epp.html', {'asignacion': asignacion})


@login_required
@user_passes_test(is_admin_or_staff, login_url='error')
def estadoEPP(request, asignado_id):
    # Obtener la instancia de PersonalEpps
    asignacion = get_object_or_404(PersonalEpps, id=asignado_id)
    
    if request.method == 'POST':
        descripcion = request.POST.get('descripcion')
        if descripcion:
            # Crear un nuevo estado para el EPP
            # EstadoEPP.objects.create(PersonalEpps=asignacion,descripcion=descripcion, reportado=timezone.now())
            nuevo_estado = EstadoEPP.objects.create(
                PersonalEpps=asignacion,
                descripcion=descripcion,
           
                reportado=timezone.now()
            )

            # Preparar los datos para el correo
            nombre_persona = asignacion.idPersonal.get_full_name() or asignacion.idPersonal.username
            nombre_epp = asignacion.idEpp.nombre
            fecha_reportado = nuevo_estado.reportado.strftime('%d/%m/%Y %H:%M:%S')

            # Crear el mensaje del correo con nombres de campos
            mensaje_correo = (
                f"Nuevo Reporte de Estado de EPP\n\n"
                f"Persona: {nombre_persona}\n"
                f"EPP: {nombre_epp}\n"
                f"Descripción: {descripcion}\n"
        
                f"Fecha Reportado: {fecha_reportado}\n"
            )

            # Enviar correo con la información del mantenimiento
            send_mail(
                subject='Nuevo Reporte de Estado de EPP',
                message=mensaje_correo,
                from_email='bomberosmunicipalestotonicapan@gmail.com',  # Asegúrate de que coincida con tu configuración
                recipient_list=['forniteb6@gmail.com'],  # Reemplaza con la dirección de correo del destinatario
                fail_silently=False,
            )
            
        return redirect('lEpp')  # Redirigir a la página principal después de guardar
    else:
        # Si el método es GET, mostrar el modal
        return render(request, 'epp.html', {"asignacion": asignacion})  # Cargar la página con la asignación


@login_required
@user_passes_test(is_admin, login_url='error')
def marcar_arregladoEPP(request, codigo):
    estado = get_object_or_404(EstadoEPP, codigo=codigo)
    estado.estado = "Bueno"  # Cambia el estado a "Bueno"
    estado.save()
    messages.success(request, "La herramienta ha sido marcada como arreglada.")
    return redirect('lEpp')  # Redirige de nuevo a la lista

@login_required
@user_passes_test(is_admin, login_url='error')
def lEpp(request):
    estados = EstadoEPP.objects.filter(estado__in=["malo", "Malo"])  # Filtrar solo los estados no arreglados
    return render(request, 'lepp.html', {"estados": estados})

@login_required
@user_passes_test(is_admin, login_url='error')
def listaEPP(request):
    epp = Epp.objects.all()
    
    return render(request, 'listaEPP.html', {"epp": epp})


@login_required
@user_passes_test(is_admin, login_url='error')
def eliminar_epp(request, codigo_epp):
    epp = get_object_or_404(Epp, codigo=codigo_epp)
    if request.method == 'POST':
        epp.delete()
        messages.success(request, 'EPP eliminado correctamente.')
        return redirect('listaEPP')  # Asegúrate de que 'lista_epps' es el nombre correcto de tu vista
    return render(request, 'listaEPP.html', {'epp': epp})



@login_required
@user_passes_test(is_admin, login_url='error')
def editar_epp(request, codigo_epp):
    epp = get_object_or_404(Epp, codigo=codigo_epp)
    if request.method == 'POST':
        form = EPPForm(request.POST, instance=epp)
        if form.is_valid():
            form.save()
            messages.success(request, 'EPP editado correctamente.')
            return redirect('listaEPP')  # Asegúrate de que 'lista_epps' es el nombre correcto de tu vista
    else:
        form = EPPForm(instance=epp)
    return render(request, 'editar_epp.html', {'form': form})