
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Insumo, MovimientoInsumo
# views.py
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
# views.py
from .forms import Insumo
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.mail import send_mail
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

def registrar_insumo_nuevo(request):
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.POST.get('nombre')
        cantidad_inicial = request.POST.get('cantidadInicial')

        # Validar datos
        if not nombre or not cantidad_inicial:
            messages.error(request, 'Por favor, completa todos los campos.')
            return redirect('registrar_insumo_nuevo')  # Asegúrate de que el nombre de la URL sea correcto

        try:
            cantidad_inicial = int(cantidad_inicial)
        except ValueError:
            messages.error(request, 'La cantidad inicial debe ser un número.')
            return redirect('registrar_insumo_nuevo')

        # Obtener el usuario autenticado
        personal = request.user

        # Crear Insumo
        insumo = Insumo.objects.create(
            nombre=nombre,
            stock_inicial=cantidad_inicial,
            stock_actual=cantidad_inicial
        )

        # Registrar movimiento inicial
        MovimientoInsumo.objects.create(
            insumo=insumo,
            idPersonal=personal,
            cantidad=cantidad_inicial,
            tipo_movimiento='ENTRADA',
            observacion='Stock inicial'
        )

        messages.success(request, 'Insumo registrado exitosamente.')
        return redirect('registrar_insumo_nuevo')  # Redirigir a la misma página o donde desees

    # Para solicitudes GET, pasar insumos al contexto
    insumos = Insumo.objects.all()
    return render(request, 'insumosNuevo.html', {
        'insumos': insumos
    })





@login_required
@user_passes_test(is_admin, login_url='error')
def eliminar_insumo(request, insumo_id):
    insumo = get_object_or_404(Insumo, codigo=insumo_id)
    if request.method == 'POST':
        insumo.delete()
        return redirect('registrar_insumo_nuevo') 
    return render(request, 'registrar_insumo_nuevo.html')





@login_required
@user_passes_test(is_admin_or_staff, login_url='error')
def ajustar_stock(request, codigo):
    try:
        insumo = Insumo.objects.get(codigo=codigo)
        
        if request.method == 'POST':
            cantidad = request.POST.get('cantidad')
            tipo_movimiento = request.POST.get('tipo_movimiento')
            observacion = request.POST.get('observacion', '')
            
            # Validar cantidad
            try:
                cantidad = int(cantidad)
                if cantidad <= 0:
                    raise ValueError
            except ValueError:
                messages.error(request, 'La cantidad debe ser un número positivo.')
                return redirect('registrar_insumo_nuevo')
            
            if tipo_movimiento == 'SALIDA' and cantidad > insumo.stock_actual:
                messages.error(request, 'No hay suficiente stock disponible.')
                return redirect('registrar_insumo_nuevo')
            
            # Actualizar stock
            if tipo_movimiento == 'ENTRADA':
                insumo.stock_actual += cantidad
            else:  # SALIDA
                insumo.stock_actual -= cantidad
            
            insumo.save()
            
            # Registrar movimiento
            MovimientoInsumo.objects.create(
                insumo=insumo,
                idPersonal=request.user,  # Asumiendo que el usuario está autenticado
                cantidad=cantidad,
                tipo_movimiento=tipo_movimiento,
                observacion=observacion
            )
                       # Enviar correo si el stock es igual o menor a 10
            if insumo.stock_actual <= 10:
                
                send_mail(
                    
                subject = f"Advertencia: Bajo stock del insumo {insumo.nombre}",
                message = f"El insumo {insumo.nombre} tiene un stock actual de {insumo.stock_actual}. Por favor, revisa el inventario.",
                from_email='bomberosmunicipalestotonicapan@gmail.com',  # Cambia por el correo al que quieres enviar
                recipient_list=['forniteb6@gmail.com'],
                fail_silently=False,
                
                )
                
                
                
                
            messages.success(request, f'Stock ajustado correctamente. Nuevo stock: {insumo.stock_actual}')
            return redirect('registrar_insumo_nuevo')
                
    except Insumo.DoesNotExist:
        messages.error(request, 'Insumo no encontrado.')
        return redirect('registrar_insumo_nuevo')

@login_required
@user_passes_test(is_admin, login_url='error')
def detalle_insumo(request, codigo):
    try:
        insumo = Insumo.objects.get(codigo=codigo)
        movimientos = MovimientoInsumo.objects.filter(insumo=insumo).order_by('-fecha')
        return render(request, 'lInsumos.html', {
            'insumo': insumo,
            'movimientos': movimientos
        })
    except Insumo.DoesNotExist:
        messages.error(request, 'Insumo no encontrado')
        return redirect('registrar_insumo_nuevo')
    
    
    
