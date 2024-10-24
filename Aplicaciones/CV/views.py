from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import CVForm

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import CV, Experiencia, Certificado
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from django.http import HttpResponse, HttpResponseForbidden
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from Aplicaciones.user.models import Profile
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
# Funciones auxiliares para verificar permisos
def is_admin(user):
    return user.groups.filter(name='Administrador').exists()

def is_staff(user):
    return user.groups.filter(name='Personal').exists()


@login_required
@user_passes_test(is_admin, login_url='error')
def prueba2(request):
    object_list = User.objects.filter(profile__is_internal=True, cv__isnull=False).select_related('profile', 'cv')
    return render(request, 'prueba2.html', {"object_list": object_list})
 

@login_required
@user_passes_test(is_admin_or_staff, login_url='error')
def editar_cv(request):
    cv_instance, created = CV.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = CVForm(request.POST, instance=cv_instance)
        if form.is_valid():
            form.save()
            return redirect('perfil')  # Reemplaza 'perfil' con el nombre de tu URL
    else:
        form = CVForm(instance=cv_instance)
    return render(request, 'editar_cv.html', {'form': form})
from .forms import ExperienciaForm

@login_required
@user_passes_test(is_admin_or_staff, login_url='error')
def agregar_experiencia(request):
    cv_instance, created = CV.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ExperienciaForm(request.POST)
        if form.is_valid():
            experiencia = form.save(commit=False)
            experiencia.cv = cv_instance
            experiencia.save()
            return redirect('perfil')
    else:
        form = ExperienciaForm()
    return render(request, 'agregar_experiencia.html', {'form': form})

@login_required
@user_passes_test(is_admin_or_staff, login_url='error')
def editar_experiencia(request, experiencia_id):
    experiencia = get_object_or_404(Experiencia, id=experiencia_id, cv__user=request.user)
    if request.method == 'POST':
        form = ExperienciaForm(request.POST, instance=experiencia)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = ExperienciaForm(instance=experiencia)
    return render(request, 'editar_experiencia.html', {'form': form})

@login_required
@user_passes_test(is_admin_or_staff, login_url='error')
def eliminar_experiencia(request, experiencia_id):
    experiencia = get_object_or_404(Experiencia, id=experiencia_id, cv__user=request.user)
    if request.method == 'POST':
        experiencia.delete()
        return redirect('perfil')
    return render(request, 'eliminar_experiencia.html', {'experiencia': experiencia})
from .forms import CertificadoForm

@login_required
@user_passes_test(is_admin_or_staff, login_url='error')
def agregar_certificado(request):
    cv_instance, created = CV.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = CertificadoForm(request.POST)
        if form.is_valid():
            certificado = form.save(commit=False)
            certificado.cv = cv_instance
            certificado.save()
            return redirect('perfil')
    else:
        form = CertificadoForm()
    return render(request, 'agregar_certificado.html', {'form': form})

@login_required
@user_passes_test(is_admin_or_staff, login_url='error')
def editar_certificado(request, certificado_id):
    certificado = get_object_or_404(Certificado, id=certificado_id, cv__user=request.user)
    if request.method == 'POST':
        form = CertificadoForm(request.POST, instance=certificado)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = CertificadoForm(instance=certificado)
    return render(request, 'editar_certificado.html', {'form': form})

@login_required
@user_passes_test(is_admin_or_staff, login_url='error')
def eliminar_certificado(request, certificado_id):
    certificado = get_object_or_404(Certificado, id=certificado_id, cv__user=request.user)
    if request.method == 'POST':
        certificado.delete()
        return redirect('perfil')
    return render(request, 'eliminar_certificado.html', {'certificado': certificado})


@login_required
@user_passes_test(is_admin_or_staff, login_url='error')
def perfil(request):
    cv_instance, created = CV.objects.get_or_create(user=request.user)
    experiencias = cv_instance.experiencias.all()
    certificados = cv_instance.certificados.all()
    return render(request, 'perfil.html', {
        'cv': cv_instance,
        'experiencias': experiencias,
        'certificados': certificados,
    })
    



@login_required
@user_passes_test(is_admin_or_staff, login_url='error')
def generar_cv_reportlab_individual(request):
    # Obtener el CV del usuario
    cv_instance, created = CV.objects.get_or_create(user=request.user)
    experiencias = cv_instance.experiencias.all()
    certificados = cv_instance.certificados.all()
    
    # Crear una respuesta HTTP con el tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="CV.pdf"'
    
    # Crear el documento
    doc = SimpleDocTemplate(response, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    
    # Obtener y personalizar estilos
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='TitleStyle', fontSize=24, leading=28, alignment=TA_CENTER, spaceAfter=20, textColor=colors.HexColor("#003366")))
    styles.add(ParagraphStyle(name='HeadingStyle', fontSize=18, leading=22, spaceBefore=15, spaceAfter=10, textColor=colors.HexColor("#003366")))
    styles.add(ParagraphStyle(name='SubHeadingStyle', fontSize=14, leading=18, spaceBefore=10, spaceAfter=5, textColor=colors.HexColor("#005599")))
    styles.add(ParagraphStyle(name='NormalStyle', fontSize=12, leading=15, spaceAfter=8, textColor=colors.black))
    styles.add(ParagraphStyle(name='ItalicStyle', fontSize=12, leading=15, spaceAfter=8, textColor=colors.black, fontName='Helvetica-Oblique'))
    
    Story = []
    
    # Título
    Story.append(Paragraph(f"Currículum Vitae de {request.user.profile.name1} {request.user.profile.name2} {request.user.profile.lastname1}{request.user.profile.lastname2}", styles['TitleStyle']))
    Story.append(Spacer(1, 12))
    
    # Información Personal
    Story.append(Paragraph("Información Personal", styles['HeadingStyle']))
    
    # Tabla para la información personal y la imagen
    personal_data = []
    # Añadir imagen del perfil si existe
    if hasattr(request.user, 'profile') and request.user.profile.image:
        image_path = request.user.profile.image.url
        img = Image(image_path, width=4*cm, height=4*cm)
        img.hAlign = 'LEFT'
    else:
        img = Spacer(4*cm, 4*cm)
    
    # Datos personales
    personal_info = [
        ['Cargo:', cv_instance.cargo],
        ['Sobre mí:', cv_instance.sobre_mi],
        ['Tipo de Sangre:', cv_instance.tipo_sangre],
        ['Email:', cv_instance.contacto_email],
        ['Teléfono Emergencia:', cv_instance.contacto_telefono_emergencia],
        ['Habilidades:', cv_instance.habilidades],
        ['Estado:', cv_instance.estado],
    ]
    
    table = Table(personal_info, colWidths=[5*cm, 10*cm])
    table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 12),
        ('ALIGN', (0,0), (0,-1), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    
    # Combinar imagen y tabla en una tabla principal
    main_table = Table([[img, table]], colWidths=[5*cm, 12*cm])
    main_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    
    Story.append(main_table)
    Story.append(Spacer(1, 12))
    Story.append(Paragraph('<hr width="100%" color="#003366"/>', styles['Normal']))
    Story.append(Spacer(1, 12))
    
    # Experiencias
    Story.append(Paragraph("Experiencias Profesionales", styles['HeadingStyle']))
    for experiencia in experiencias:
        exp_title = f"<b>{experiencia.puesto}</b> en {experiencia.empresa}"
        exp_period = f"{experiencia.fecha_inicio.strftime('%b %Y')} - {experiencia.fecha_fin.strftime('%b %Y') if experiencia.fecha_fin else 'Presente'}"
        Story.append(Paragraph(exp_title, styles['SubHeadingStyle']))
        Story.append(Paragraph(exp_period, styles['ItalicStyle']))
        Story.append(Paragraph(experiencia.descripcion, styles['NormalStyle']))
        Story.append(Spacer(1, 6))
    
    Story.append(Spacer(1, 12))
    Story.append(Paragraph('<hr width="100%" color="#003366"/>', styles['Normal']))
    Story.append(Spacer(1, 12))
    
    # Certificados
    Story.append(Paragraph("Certificados", styles['HeadingStyle']))
    for certificado in certificados:
        cert_title = f"<b>{certificado.titulo}</b>"
        Story.append(Paragraph(cert_title, styles['SubHeadingStyle']))
        Story.append(Paragraph(certificado.descripcion, styles['NormalStyle']))
        if certificado.url_archivo:
            # Crear un enlace clicable con estilo
            link = f'<link href="{certificado.url_archivo}" color="#1a0dab">Ver Certificado PDF</link>'
            Story.append(Paragraph(link, styles['NormalStyle']))
        Story.append(Spacer(1, 6))
    

    # Construir el PDF
    doc.build(Story)
    
    return response





@login_required
@user_passes_test(is_admin_or_staff, login_url='error')
def generar_cv_reportlab_platypus(request, user_id):
    # Obtener el usuario específico que es interno
    user_profile = get_object_or_404(User, id=user_id, profile__is_internal=True)

    # # Permitir solo al propietario del CV o a usuarios con permisos especiales (por ejemplo, staff) generar el PDF
    # if request.user != user_profile and not request.user.is_staff:
    #     return HttpResponseForbidden("No tienes permiso para generar este CV.")

    # Obtener o crear el CV asociado al usuario
    cv_instance, created = CV.objects.get_or_create(user=user_profile)
    experiencias = cv_instance.experiencias.all()
    certificados = cv_instance.certificados.all()

    # Crear una respuesta HTTP con el tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="CV_{user_profile.username}.pdf"'

    # Crear el documento
    doc = SimpleDocTemplate(
        response,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    # Obtener y personalizar estilos
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='TitleStyle',
        fontSize=24,
        leading=28,
        alignment=TA_CENTER,
        spaceAfter=20,
        textColor=colors.HexColor("#003366")
    ))
    styles.add(ParagraphStyle(
        name='HeadingStyle',
        fontSize=18,
        leading=22,
        spaceBefore=15,
        spaceAfter=10,
        textColor=colors.HexColor("#003366")
    ))
    styles.add(ParagraphStyle(
        name='SubHeadingStyle',
        fontSize=14,
        leading=18,
        spaceBefore=10,
        spaceAfter=5,
        textColor=colors.HexColor("#005599")
    ))
    styles.add(ParagraphStyle(
        name='NormalStyle',
        fontSize=12,
        leading=15,
        spaceAfter=8,
        textColor=colors.black
    ))
    styles.add(ParagraphStyle(
        name='ItalicStyle',
        fontSize=12,
        leading=15,
        spaceAfter=8,
        textColor=colors.black,
        fontName='Helvetica-Oblique'
    ))

    Story = []

    # Título
    Story.append(Paragraph(f"Currículum Vitae de {user_profile.profile.name1}", styles['TitleStyle']))
    Story.append(Spacer(1, 12))

    # Información Personal
    Story.append(Paragraph("Información Personal", styles['HeadingStyle']))

    # Tabla para la información personal y la imagen
    personal_data = []
    # Añadir imagen del perfil si existe
    if hasattr(user_profile, 'profile') and user_profile.profile.image:
        image_path = request.user.profile.image.url
        try:
            img = Image(image_path, width=4*cm, height=4*cm)
            img.hAlign = 'LEFT'
        except Exception as e:
            print(f"Error al añadir la imagen: {e}")
            img = Spacer(4*cm, 4*cm)
    else:
        img = Spacer(4*cm, 4*cm)

    # Datos personales
    personal_info = [
        ['Cargo:', cv_instance.cargo],
        ['Sobre mí:', cv_instance.sobre_mi],
        ['Tipo de Sangre:', cv_instance.tipo_sangre],
        ['Email:', cv_instance.contacto_email],
        ['Teléfono Emergencia:', cv_instance.contacto_telefono_emergencia],
        ['Habilidades:', cv_instance.habilidades],
        ['Estado:', cv_instance.estado],
    ]

    table = Table(personal_info, colWidths=[5*cm, 10*cm])
    table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 12),
        ('ALIGN', (0,0), (0,-1), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))

    # Combinar imagen y tabla en una tabla principal
    main_table = Table([[img, table]], colWidths=[5*cm, 12*cm])
    main_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))

    Story.append(main_table)
    Story.append(Spacer(1, 12))
    Story.append(Paragraph('<hr width="100%" color="#003366"/>', styles['Normal']))
    Story.append(Spacer(1, 12))

    # Experiencias
    Story.append(Paragraph("Experiencias Profesionales", styles['HeadingStyle']))
    for experiencia in experiencias:
        exp_title = f"<b>{experiencia.puesto}</b> en {experiencia.empresa}"
        exp_period = f"{experiencia.fecha_inicio.strftime('%b %Y')} - {experiencia.fecha_fin.strftime('%b %Y') if experiencia.fecha_fin else 'Presente'}"
        Story.append(Paragraph(exp_title, styles['SubHeadingStyle']))
        Story.append(Paragraph(exp_period, styles['ItalicStyle']))
        Story.append(Paragraph(experiencia.descripcion, styles['NormalStyle']))
        Story.append(Spacer(1, 6))

    Story.append(Spacer(1, 12))
    Story.append(Paragraph('<hr width="100%" color="#003366"/>', styles['Normal']))
    Story.append(Spacer(1, 12))

    # Certificados
    Story.append(Paragraph("Certificados", styles['HeadingStyle']))
    for certificado in certificados:
        cert_title = f"<b>{certificado.titulo}</b>"
        Story.append(Paragraph(cert_title, styles['SubHeadingStyle']))
        Story.append(Paragraph(certificado.descripcion, styles['NormalStyle']))
        if certificado.url_archivo:
            # Crear un enlace clicable con estilo
            link = f'<a href="{certificado.url_archivo}" color="#1a0dab">Ver Certificado PDF</a>'
            Story.append(Paragraph(link, styles['NormalStyle']))
        Story.append(Spacer(1, 6))


    try:
        doc.build(Story)
    except Exception as e:
        print(f"Error al construir el PDF: {e}")

    return response




@login_required
@user_passes_test(is_admin, login_url='error')
def prueba(request):
    users_with_cv = User.objects.filter(profile__is_internal=True, cv__isnull=False).select_related('profile', 'cv')
    return render(request, 'prueba.html', {"object_list": users_with_cv})


@login_required
@user_passes_test(is_admin, login_url='error')
def perfil_cv(request, user_id):
    # Obtener el usuario específico que es interno
    user_profile = get_object_or_404(User, id=user_id, profile__is_internal=True)
    
    # Obtener o crear el CV asociado al usuario
    cv_instance, created = CV.objects.get_or_create(user=user_profile)
    
    # Obtener experiencias y certificados asociados al CV
    experiencias = cv_instance.experiencias.all()
    certificados = cv_instance.certificados.all()
    
    return render(request, 'perfil_cv.html', {
        'cv': cv_instance,
        'experiencias': experiencias,
        'certificados': certificados,
        'user_profile': user_profile,  # Renombrado para evitar conflictos con `request.user`
    })