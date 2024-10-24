from django.shortcuts import render, redirect
from django.views import View
from .forms import ServicioForm, VariosForm, AmbulanciaForm, IncendiosForm,CategoriasEmergenciasForm
from .models import Servicio
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from .models import Ambulancia
from django.contrib import messages
from .models import Servicio, Varios, Ambulancia, Incendios, Categorias_emergencias
from django.contrib.staticfiles import finders
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied


def prueba_catr(request):
    # Agrega un print para debug
    print("Vista listar_categorias ejecutándose")
    categorias = Categorias_emergencias.objects.all()
    # Agrega otro print para ver si hay categorías
    print(f"Categorías encontradas: {categorias.count()}")
    return render(request, 'prueba_catr.html', {'categorias': categorias})



# servcios varios acciones
def eliminar_servicio_vario(request, servicio_id):
    servicio_vario = get_object_or_404(Varios, id=servicio_id)
    if request.method == 'POST':
        servicio_vario.delete()
        return redirect('varios') 
    return render(request, 'varios.html')

@login_required
def editar_servicio_vario(request, servicio_id, vario_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)
    vario = get_object_or_404(Varios, id=vario_id)

    if request.method == 'POST':
        servicio_form = ServicioForm(request.POST, instance=servicio)
        vario_form = IncendiosForm(request.POST, instance=vario)

        if servicio_form.is_valid() and vario_form.is_valid():
            servicio_form.save()
            vario_form.save()
            messages.success(request, 'Servicios varios editados correctamente.')
            return redirect('varios')  # Asegúrate de que esta es la URL correcta
    else:
        servicio_form = ServicioForm(instance=servicio)
        vario_form = VariosForm(instance=vario)

    return render(request, 'editar_varios.html', {
        'servicio_form': servicio_form,
        'vario_form': vario_form
    })
    
    # servicio ambulancia acciones
def eliminar_servicio_ambulancia(request, servicio_id):
    servicio_ambulancia = get_object_or_404(Ambulancia, id=servicio_id)
    if request.method == 'POST':
        servicio_ambulancia.delete()
        return redirect('ambulancia') 
    return render(request, 'ambulancia.html')

@login_required
def editar_servicio_ambulancia(request, servicio_id, ambulancia_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)
    ambulancia = get_object_or_404(Ambulancia, id=ambulancia_id)

    if request.method == 'POST':
        servicio_form = ServicioForm(request.POST, instance=servicio)
        ambulancia_form = AmbulanciaForm(request.POST, instance=ambulancia)

        if servicio_form.is_valid() and ambulancia_form.is_valid():
            servicio_form.save()
            ambulancia_form.save()
            messages.success(request, 'Servicio y incendios editados correctamente.')
            return redirect('ambulancia')  # Asegúrate de que esta es la URL correcta
    else:
        servicio_form = ServicioForm(instance=servicio)
        ambulancia_form = AmbulanciaForm(instance=ambulancia)

    return render(request, 'editar_ambulancia.html', {
        'servicio_form': servicio_form,
        'ambulancia_form': ambulancia_form
    })
    
#    servicios incendios acciones
def eliminar_servicio_incendios(request, servicio_id):
    servicio_incendios = get_object_or_404(Incendios, id=servicio_id)
    if request.method == 'POST':
        servicio_incendios.delete()
        return redirect('incendios') 
    return render(request, 'incendios.html')

@login_required
def editar_servicio_incendios(request, servicio_id, incendio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)
    incendio = get_object_or_404(Incendios, id=incendio_id)

    if request.method == 'POST':
        servicio_form = ServicioForm(request.POST, instance=servicio)
        incendio_form = IncendiosForm(request.POST, instance=incendio)

        if servicio_form.is_valid() and incendio_form.is_valid():
            servicio_form.save()
            incendio_form.save()
            messages.success(request, 'Servicio de incendio editados correctamente.')
            return redirect('incendios')  # Asegúrate de que esta es la URL correcta
    else:
        servicio_form = ServicioForm(instance=servicio)
        incendio_form = IncendiosForm(instance=incendio)

    return render(request, 'editar_incendio.html', {
        'servicio_form': servicio_form,
        'incendio_form': incendio_form
    }) 
    
    





# Vista para crear una nueva categoría
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriasEmergenciasForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('prueba_catr')
    else:
        form = CategoriasEmergenciasForm()
    return render(request, 'crear.html', {'form': form})


    
def is_admin_or_staff(user):
    return user.is_authenticated and user.groups.filter(name__in=['Administrador', 'Personal']).exists()

logo_derecha = finders.find('img/images.png')

from collections import defaultdict
from django.shortcuts import render
from .models import Ambulancia, Categorias_emergencias

def reporte_ambulancia(request):
    # Obtenemos todos los registros de Ambulancia
    ambulancias = Ambulancia.objects.select_related('servicio', 'codigo_emergencia')

    # Agrupamos por mes y código de emergencia manualmente usando defaultdict
    reportes = defaultdict(lambda: defaultdict(int))  # Estructura: {año-mes: {codigo_emergencia: total}}

    for ambulancia in ambulancias:
        # Obtenemos el año y mes desde el campo fecha_hora
        año_mes = ambulancia.servicio.fecha_hora.strftime('%Y-%m')
        codigo_emergencia = ambulancia.codigo_emergencia.id
        reportes[año_mes][codigo_emergencia] += 1

    # Formateamos los resultados para enviarlos al template
    resultados = []
    for año_mes, emergencias in reportes.items():
        for codigo, total in emergencias.items():
            # Obtenemos el nombre correcto de la emergencia por el código
            nombre = Categorias_emergencias.objects.get(id=codigo).nombre
            resultados.append({
                'codigo': codigo,
                'nombre': nombre,
                'total': total,
                'fecha': año_mes  # Fecha en formato 'Año-Mes'
            })
    
    return render(request, 'reporte_ambulancia.html', {'resultados': resultados})





@login_required
@user_passes_test(is_admin_or_staff, login_url='error')
def servicio_create_view(request):
    if request.method == 'POST':
        servicio_form = ServicioForm(request.POST)
        varios_form = VariosForm(request.POST, prefix='varios')
        ambulancia_form = AmbulanciaForm(request.POST, prefix='ambulancia')
        incendios_form = IncendiosForm(request.POST, prefix='incendios')
        
        servicio_choice = request.POST.get('servicio')
        form_mapping = {
            '1': varios_form,
            '2': ambulancia_form,
            '3': incendios_form,
        }
        
        if servicio_form.is_valid():
            servicio = servicio_form.save()
            selected_form = form_mapping.get(servicio_choice)
            if selected_form and selected_form.is_valid():
                instance = selected_form.save(commit=False)
                instance.servicio = servicio
                instance.save()
                return redirect(reverse('add'))
        
        # Si hay errores, renderizar la plantilla nuevamente con los formularios
        return render(request, 'add.html', {
            'servicio_form': servicio_form,
            'varios_form': varios_form,
            'ambulancia_form': ambulancia_form,
            'incendios_form': incendios_form,
        })
    
    else:
        servicio_form = ServicioForm()
        varios_form = VariosForm(prefix='varios')
        ambulancia_form = AmbulanciaForm(prefix='ambulancia')
        incendios_form = IncendiosForm(prefix='incendios')
        return render(request, 'add.html', {
            'servicio_form': servicio_form,
            'varios_form': varios_form,
            'ambulancia_form': ambulancia_form,
            'incendios_form': incendios_form,
        })

        
@login_required
@user_passes_test(is_admin_or_staff, login_url='error')
def varios_list_view(request):
    varios_list = Varios.objects.filter(servicio__activo=True)
    # Get the choices for the service field
    servicio_choices = Varios._meta.get_field('servicio').choices
    
    context = {
        'varios': varios_list,
        'servicio_choices': servicio_choices,
    }
    return render(request, 'varios.html', context)

def ambulancia_list_view(request):
    ambulancias = Ambulancia.objects.all()
    return render(request, 'ambulancia.html', {'ambulancias': ambulancias})

def incendios_list_view(request):
    incendios = Incendios.objects.all()
    return render(request, 'incendios.html', {'incendios': incendios})

def servicio_list_view(request):
    servicios = Servicio.objects.all()
    return render(request, 'servicio_lista.html', {'servicios': servicios})

# views.py

@login_required
@user_passes_test(is_admin_or_staff, login_url='error')
def editar_desactivar_varios(request, pk):
    varios = get_object_or_404(Varios, pk=pk)
    servicio = varios.servicio  # Relación con Servicio

    if request.method == 'POST':
        accion = request.POST.get('accion')

        if accion == 'editar':
            servicio_form = ServicioForm(request.POST, instance=servicio)
            varios_form = VariosForm(request.POST, instance=varios)

            if servicio_form.is_valid() and varios_form.is_valid():
                servicio_form.save()
                varios_form.save()
                messages.success(request, 'Servicio actualizado correctamente.')
            else:
                messages.error(request, 'Por favor corrige los errores en el formulario.')

        elif accion == 'desactivar':
            servicio.activo = False
            servicio.save()
            messages.success(request, 'Servicio desactivado correctamente.')

        return redirect('varios')  # Reemplaza con el nombre correcto de tu URL

    # Si el método no es POST, redirigir a la lista
    return redirect('varios')


from .models import Servicio
@login_required
@user_passes_test(is_admin_or_staff, login_url='error')
def tabla_servicios(request):
    servicios = Servicio.objects.filter(activo=True).values(
        'piloto',
        'unidad',
        'salida_hora',
        'entrada_hora',
        'direccion',
        'servicio',
        'observaciones'
    )
    return render(request, 'unificado.html', {'servicios': servicios})

@login_required
@user_passes_test(is_admin_or_staff, login_url='error')
def vista_kilometraje(request):
    servicios = Servicio.objects.filter(activo=True).values(
        'unidad',
        'salida_hora',
        'entrada_hora',
        'km_recorridos',
        
    )
    # Para calcular 'hrs', es mejor obtener los objetos completos
    servicios = Servicio.objects.filter(activo=True)
    return render(request, 'vista_kilometraje.html', {'servicios': servicios})



@login_required
@user_passes_test(is_admin_or_staff, login_url='error')
# CODIGO PARA GENERAR REPORTES SEGUN SEA EL SERVICIO
def generar_reporte_servicios_varios(request, varios_id):
    varios = get_object_or_404(Varios, id=varios_id)
    servicio = varios.servicio

    # Crear una respuesta HTTP con el tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporte_servicios_varios_{varios_id}.pdf"'

    # Crear el objeto PDF
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Ajustar las coordenadas para empezar desde la parte superior
    y = height - 50

    # Agregar logotipos (ajustar las rutas a las imágenes que subiste)
    logo_izquierda = finders.find('img/images2.png')
    logo_derecha = finders.find('img/images.png')

    # Posicionar logos
    p.drawImage(logo_izquierda, 50, height - 80, width=60, height=60)
    p.drawImage(logo_derecha, width - 110, height - 80, width=60, height=60)

    # Título principal centrado
    p.setFont("Helvetica-Bold", 10)
    p.drawCentredString(width / 2, y, "ASOCIACIÓN NACIONAL DE BOMBEROS")
    p.drawCentredString(width / 2, y - 20, "MUNICIPALES DEPARTAMENTALES")
    p.drawCentredString(width / 2, y - 40, "(ASONBOMD)")
    p.drawCentredString(width / 2, y - 60, "SERVICIO VARIOS")

    # Reducir el tamaño de la letra para el contenido
    p.setFont("Helvetica", 10)
    y = height - 170  # Ajustar la posición después del título

    # Información General
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Estación:")
    p.drawString(300, y, "Turno:")
    p.drawString(450, y, "Fecha:")
    p.setFont("Helvetica", 10)
    p.drawString(120, y, f"{servicio.estacion}")
    p.drawString(360, y, f"{servicio.turno}")
    p.drawString(510, y, f"{varios.fecha.strftime('%d/%m/%Y')}")

    y -= 20

    # Dirección
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Dirección:")
    p.setFont("Helvetica", 10)
    p.drawString(150, y, f"{servicio.direccion}")

    y -= 20

    # Servicio de, salida, entrada
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Servicio de:")
    p.drawString(300, y, "Salida:")
    p.drawString(450, y, "Entrada:")
    p.setFont("Helvetica", 10)
    p.drawString(150, y, f"{varios.servicio_de}")
    p.drawString(350, y, f"{servicio.salida_hora.strftime('%H:%M')}")
    p.drawString(510, y, f"{servicio.entrada_hora.strftime('%H:%M')}")

    y -= 20

    # Jefe de Servicio y Telefonista
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Jefe de Servicio:")
    p.drawString(300, y, "Telefonista de turno:")
    p.setFont("Helvetica", 10)
    p.drawString(150, y, f"{varios.jefe_servicio}")
    p.drawString(400, y, f"{servicio.telefonista}")

    y -= 20

    # Bombero, Unidad, Piloto
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Bombero que reporta:")
    p.drawString(300, y, "Unidad:")
    p.drawString(450, y, "Piloto:")
    p.setFont("Helvetica", 10)
    p.drawString(180, y, f"{servicio.bombero_reporta}")
    p.drawString(350, y, f"{servicio.unidad}")
    p.drawString(510, y, f"{servicio.piloto}")

    y -= 20

    # Servicio autorizado y personal asistente
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Servicio autorizado por:")
    p.drawString(300, y, "Personal asistente:")
    p.setFont("Helvetica", 10)
    p.drawString(200, y, f"{varios.servicio_autorizado_por}")
    p.drawString(450, y, f"{servicio.personal_asistente}")

    y -= 40

    # Observaciones
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Observaciones:")
    p.setFont("Helvetica", 10)
    p.drawString(150, y, f"{servicio.observaciones}")

    # Dibujo de líneas para las observaciones
    p.line(50, y - 10, 550, y - 10)
    p.line(50, y - 30, 550, y - 30)
    p.line(50, y - 50, 550, y - 50)

    y -= 70

    # Sección de Kilometraje
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Kilometraje de entrada:")
    p.setFont("Helvetica", 10)
    p.drawString(200, y, f"{servicio.km_entrada}")
    p.drawString(250, y, "Guatemala, __________________________________")

    y -= 20

    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Kilometraje de salida:")
    p.setFont("Helvetica", 10)
    p.drawString(200, y, f"{servicio.km_salida}")
    p.drawString(250, y, "(f) Bombero                   No.: _______________")

    y -= 20

    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Kilómetros recorridos:")
    p.setFont("Helvetica", 10)
    p.drawString(200, y, f"{servicio.km_recorridos}")

    # Finalizar PDF
    p.showPage()
    p.save()
    return response




@login_required
@user_passes_test(is_admin_or_staff, login_url='error')
def generar_reporte_ambulancia(request, ambulancia_id):
    ambulancia = get_object_or_404(Ambulancia, id=ambulancia_id)
    servicio = ambulancia.servicio

    # Crear una respuesta HTTP con el tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporte_ambulancia_{ambulancia_id}.pdf"'

    # Crear el objeto PDF
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Ajustar las coordenadas para empezar desde la parte superior
    y = height - 50

    # Agregar logotipos
    logo_izquierda = finders.find('img/images2.png')
    logo_derecha = finders.find('img/images.png')

    # Logotipos a la izquierda y derecha
    p.drawImage(logo_izquierda, 50, height - 80, width=60, height=60)
    p.drawImage(logo_derecha, width - 110, height - 80, width=60, height=60)

    # Centrar títulos
    p.setFont("Helvetica-Bold", 10)
    p.drawCentredString(width / 2, y, "ASOCIACIÓN NACIONAL DE BOMBEROS")
    p.drawCentredString(width / 2, y - 20, "MUNICIPALES DEPARTAMENTALES")
    p.drawCentredString(width / 2, y - 40, "(ASONBOMD)")
    p.drawCentredString(width / 2, y - 60, "SERVICIO DE AMBULANCIA")

    # Reducir el tamaño de la letra para el contenido
    p.setFont("Helvetica", 10)
    y = height - 170  # Ajustar la posición después del título

    # Sección 1: Estación, Turno y Código
    p.setFont("Helvetica-Bold", 10)
    # p.drawString(20, y, "Firma Jefe del Servicio: _______________")
    p.drawString(50, y, "Estación:")
    p.drawString(200, y, "Turno:")
    p.drawString(300, y, "Código:")
    p.setFont("Helvetica", 10)
    p.drawString(110, y, f"{servicio.estacion}")
    p.drawString(250, y, f"{servicio.turno}")
    p.drawString(350, y, f"{ambulancia.codigo_emergencia.id}")

    y -= 20

    # Sección 2: Dirección, Paciente
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Dirección del traslado:")
    p.drawString(50, y - 20, "Nombre del paciente:")
    p.drawString(50, y - 40, "Dirección del paciente:")
    p.setFont("Helvetica", 10)
    p.drawString(200, y, f"{ambulancia.traslado_a}")
    p.drawString(200, y - 20, f"{ambulancia.nombre_paciente}")
    p.drawString(200, y - 40, f"{ambulancia.direccion_paciente}")

    y -= 60

    # Sección 3: Edad, Sexo y Traslado
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Edad:")
    p.drawString(200, y, "Sexo:")
    p.drawString(350, y, "Se trasladó a:")
    p.setFont("Helvetica", 10)
    p.drawString(100, y, f"{ambulancia.edad}")
    p.drawString(250, y, f"{ambulancia.sexo}")
    p.drawString(450, y, f"{servicio.estacion}")

    y -= 20

    # Sección 4: Forma de aviso, Telefonista
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Forma de aviso:")
    p.drawString(250, y, "Telefonista de turno:")
    p.setFont("Helvetica", 10)
    p.drawString(150, y, f"{ambulancia.forma_aviso}")
    p.drawString(400, y, f"{servicio.telefonista}")

    y -= 20

    # Sección 5: Bombero, Unidad, Piloto
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Bombero que reporta:")
    p.drawString(250, y, "Unidad:")
    p.drawString(400, y, "Piloto:")
    p.setFont("Helvetica", 10)
    p.drawString(200, y, f"{servicio.bombero_reporta}")
    p.drawString(300, y, f"{servicio.unidad}")
    p.drawString(450, y, f"{servicio.piloto}")

    y -= 20

    # Sección 6: Salida, Hora efectiva, Entrada
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Salida:")
    p.drawString(150, y, "Hora efectiva del servicio:")
    p.drawString(400, y, "Entrada:")
    p.setFont("Helvetica", 10)
    p.drawString(100, y, f"{servicio.salida_hora.strftime('%H:%M')}")
    p.drawString(300, y, f"{ambulancia.hora_efectiva_servicio.strftime('%H:%M')}")
    p.drawString(450, y, f"{servicio.entrada_hora.strftime('%H:%M')}")

    y -= 20

    # Sección 7: Asistentes y Observaciones
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Bomberos asistentes:")
    p.setFont("Helvetica", 10)
    p.drawString(200, y, f"{servicio.personal_asistente}")
    
    y -= 20
    
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Observaciones:")
    p.setFont("Helvetica", 10)
    p.drawString(200, y, f"{servicio.observaciones}")

    # Dibujo de líneas para las observaciones
    p.line(50, y - 10, 550, y - 10)
    p.line(50, y - 30, 550, y - 30)
    p.line(50, y - 50, 550, y - 50)

    y -= 70

    # Sección 8: Kilometraje
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Km entrada:")
    p.setFont("Helvetica", 10)
    p.drawString(120, y, f"{servicio.km_entrada}")
    p.drawString(200, y, "Guatemala, _____________________________________________________")

    y -= 20

    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Km salida:")
    p.setFont("Helvetica", 10)
    p.drawString(120, y, f"{servicio.km_salida}")
    p.drawString(200, y, "(f) Bombero                   No. Bombero: _______________")

    y -= 20

    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Km recorridos:")
    p.setFont("Helvetica", 10)
    p.drawString(150, y, f"{servicio.km_recorridos}")

    # Finalizar el PDF
    p.showPage()
    p.save()

    return response
@login_required
@user_passes_test(is_admin_or_staff, login_url='error')
def generar_reporte_incendios(request, incendio_id):
    incendio = get_object_or_404(Incendios, id=incendio_id)
    servicio = incendio.servicio
    # Crear una respuesta HTTP con el tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporte_incendios_{incendio_id}.pdf"'

    # Crear el objeto PDF
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Ajustar las coordenadas para empezar desde la parte superior
    y = height - 50

    # Agregar logotipos (ajustar las rutas a las imágenes que subiste)
    logo_izquierda = finders.find('img/images2.png')
    logo_derecha = finders.find('img/images.png')
    # Posicionar logos
    p.drawImage(logo_izquierda, 50, height - 80, width=60, height=60)
    p.drawImage(logo_derecha, width - 110, height - 80, width=60, height=60)

    # Título principal centrado
    # Título principal centrado
    p.setFont("Helvetica-Bold", 10)
    p.drawCentredString(width / 2, y, "ASOCIACIÓN NACIONAL DE BOMBEROS")
    p.drawCentredString(width / 2, y - 20, "MUNICIPALES DEPARTAMENTALES")
    p.drawCentredString(width / 2, y - 40, "(ASONBOMD)")
    p.drawCentredString(width / 2, y - 60, "CONTROL DE INCENDIOS ESTRUCTURALES")

    y -= 100

    # Información General
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Estación:")
    p.drawString(300, y, "Turno:")
    p.setFont("Helvetica", 10)
    p.drawString(120, y, f"{servicio.estacion}")
    p.drawString(360, y, f"{servicio.turno}")

    y -= 20

    # Ubicación del siniestro
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Ubicación del siniestro:")
    p.setFont("Helvetica", 10)
    p.drawString(180, y, f"{servicio.direccion}")

    y -= 20

    # Valor, Pérdida, Proporción, Clase de fuego
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Inmueble:")
    p.drawString(200, y, "valor:")
    p.drawString(400, y, "Perdida:")
    p.setFont("Helvetica", 10)
    p.drawString(100, y, f"{incendio.servicio_incendio_inmueble}")
    p.drawString(250, y, f"{incendio.valor}")
    p.drawString(470, y, f"{incendio.perdida}")
    y -= 20

    # Valor, Pérdida, Proporción, Clase de fuego
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Proporcion:")
    p.drawString(200, y, "Clase fuego:")
  
    p.setFont("Helvetica", 10)
    p.drawString(150, y, f"{incendio.proporcion}")
    p.drawString(300, y, f"{incendio.clase_fuego}")
    y -= 20

    # Unidades policiacas, otras instituciones
    # Valor, Pérdida, Proporción, Clase de fuego
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Salida:")
    p.drawString(200, y, "Hora efectiva del servicio:")
    p.drawString(400, y, "Entrada:")
    p.setFont("Helvetica", 10)
    p.drawString(100, y, f"{servicio.salida_hora.strftime('%H:%M')}")
    p.drawString(340, y, f"{incendio.hora_efectiva.strftime('%H:%M') }")
    p.drawString(470, y, f"{servicio.entrada_hora.strftime('%H:%M')}")
    y -= 20

    # Valor, Pérdida, Proporción, Clase de fuego
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Jefe de servicio:")
    p.drawString(300, y, "Telefonista de turno:")
  
    p.setFont("Helvetica", 10)
    p.drawString(170, y, f"{incendio.valor}")
    p.drawString(450, y, f"{incendio.perdida}")
    y -= 20
  

    # Valor, Pérdida, Proporción, Clase de fuego
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Bombero que reporta:")
    p.drawString(300, y, "Piloto:")
  
    p.setFont("Helvetica", 10)
    p.drawString(170, y, f"{servicio.bombero_reporta}")
    p.drawString(390, y, f"{servicio.piloto}")
    y -= 20
        # Valor, Pérdida, Proporción, Clase de fuego
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Unidad:")
    p.drawString(200, y, "Otras unidades asistentes de la estacion:")
  
    p.setFont("Helvetica", 10)
    p.drawString(100, y, f"{servicio.unidad}")
    p.drawString(470, y, f"{incendio.otras_unidades_asistentes_estacion}")
   
    y -= 20

    # Observaciones
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Otras unidades asistentes de otras estaciones:")
    p.setFont("Helvetica", 10)
    p.drawString(350, y, f"{incendio.unidades_asistentes_otras_estaciones}")
    y -= 20
        # Observaciones
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Personal asistente de la estacion:")
    p.setFont("Helvetica", 10)
    p.drawString(225, y, f"{servicio.personal_asistente}")
    y -= 20
        # Observaciones
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Personal de otras estaciones: ")
    p.setFont("Helvetica", 10)
    p.drawString(200, y, f"{incendio.personal_asistente_otras_estaciones}")

        # Observaciones
    y -= 70
    
   # Estilos para el párrafo
    styles = getSampleStyleSheet()
    styleN = styles['Normal']

    # Convertir el texto de observaciones en un párrafo que se ajuste
    p.setFont("Helvetica-Bold", 10)
    observaciones_paragraph = Paragraph(f"Observaciones: {servicio.observaciones}", styleN)
    
    # Ajustar coordenadas y agregar el párrafo en el PDF
    y -= 20
    observaciones_paragraph.wrapOn(p, 500, 100)  # Ajusta el ancho del bloque de texto (500 es el ancho máximo disponible)
    observaciones_paragraph.drawOn(p, 50, y)
    
    # Dibujo de líneas debajo de las observaciones
    y -= 30  # Ajusta la posición vertical dependiendo del contenido



    # Sección 8: Kilometraje
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Km entrada:")
    p.setFont("Helvetica", 10)
    p.drawString(120, y, f"{servicio.km_entrada}")
    p.drawString(200, y, "Guatemala, _____________________________________________________")

    y -= 20

    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Km salida:")
    p.setFont("Helvetica", 10)
    p.drawString(120, y, f"{servicio.km_salida}")
    p.drawString(200, y, "(f) Bombero                   No. Bombero: _______________")

    y -= 20

    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Km recorridos:")
    p.setFont("Helvetica", 10)
    p.drawString(150, y, f"{servicio.km_recorridos}")
    # Finalizar PDF
    p.showPage()
    p.save()
    return response
