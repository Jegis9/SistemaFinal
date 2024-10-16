from django.shortcuts import render, redirect, get_object_or_404
from .models import Personal, Experiencia, Habilidad, Certificacion, Educacion
from django.contrib.auth.decorators import login_required
# Vista para crear un perfil personal
from django.contrib.auth.models import User
@login_required
def personal(request, user_id):
    # Recupera el usuario basado en el user_id pasado en la URL
    user = User.objects.get(id=user_id)
    
    if request.method == 'POST':
        # Recupera los datos del formulario
        cargo = request.POST.get('cargo')
        sobre_mi = request.POST.get('sobre_mi')
        tipo_sangre = request.POST.get('tipo_sangre')
        contacto_telefono_emergencia = request.POST.get('contacto_telefono_emergencia')
        contacto_email = request.POST.get('contacto_email')
        estado = request.POST.get('estado')

        # Crea el objeto Personal (enlazando correctamente con el usuario)
        Personal.objects.create(
            user=user,  # Relaciona con el usuario recuperado
            cargo=cargo, 
            sobre_mi=sobre_mi, 
            tipo_sangre=tipo_sangre,
            contacto_telefono_emergencia=contacto_telefono_emergencia,
            contacto_email=contacto_email,
            estado=estado
        )

        return redirect('experiencia')  # Redirige a la siguiente vista
    else:
        return render(request, 'personal.html', {'user': user})



# Vista para crear experiencias
@login_required
def experiencia(request):
    if request.method == 'POST':
        # Obtener el perfil del personal (a través del ID que recibes del formulario)
        personal_id = request.POST.get('personal_id')
        personal = get_object_or_404(Personal, id=personal_id)

        descripcion = request.POST.get('descripcion')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        cargo_experiencia = request.POST.get('cargo_experiencia')

        # Crea la experiencia enlazando correctamente al objeto `Personal`
        Experiencia.objects.create(
            personal=personal,
            descripcion=descripcion,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            cargo=cargo_experiencia
        )

        return redirect('habilidades')  # Redirige a la siguiente vista
    else:
        return render(request, 'experiencia.html')


# Vista para agregar habilidades
@login_required
def habilidades(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')

        # Crear la habilidad
        Habilidad.objects.create(nombre=nombre)
        return redirect('certificaciones')  # Redirige a la siguiente vista
    else:
        return render(request, 'habilidades.html')


# Vista para crear certificaciones
@login_required
def certificaciones(request):
    if request.method == 'POST':
        personal_id = request.POST.get('personal_id')
        personal = get_object_or_404(Personal, id=personal_id)

        nombre = request.POST.get('nombre')
        institucion = request.POST.get('institucion')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        # Crear la certificación enlazando al personal
        Certificacion.objects.create(
            personal=personal,
            nombre=nombre,
            institucion=institucion,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )

        return redirect('educacion')  # Redirige a la siguiente vista
    else:
        return render(request, 'certificaciones.html')


# Vista para agregar la educación
@login_required
def educacion(request):
    if request.method == 'POST':
        personal_id = request.POST.get('personal_id')
        personal = get_object_or_404(Personal, id=personal_id)

        titulo = request.POST.get('titulo')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        # Crear la educación enlazando al personal
        Educacion.objects.create(
            personal=personal,
            titulo=titulo,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )

        return redirect('educacion')  # Redirige a la vista que desees después
    else:
        return render(request, 'educacion.html')


     
