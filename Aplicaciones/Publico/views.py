from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required #importa libreria para hacer de la pagina requerido el login para poder verla
from .forms import ProfileForm # importar el formulario donde se encuentra laclase para actualizar y mostrar errores
from .models import Emergencias
from django.contrib import messages
# Create your views here.
from django.http import HttpResponse

@login_required
def reportEmergency(request):
    return render(request, 'reportEmergency.html')



import logging

logger = logging.getLogger(__name__)

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            try:
                profile = form.save(commit=False)
                if 'image' in request.FILES:
                    logger.debug(f"Attempting to save image: {request.FILES['image']}")
                    profile.image = request.FILES['image']
                profile.save()
                logger.debug(f"Profile saved. Image path: {profile.image.name}")
                return redirect('profile')
            except Exception as e:
                logger.error(f"Error saving profile: {str(e)}")
                # Manejar el error apropiadamente
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {'form': form})

@login_required
def profile_Interno(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            try:
                profile = form.save(commit=False)
                if 'image' in request.FILES:
                    profile.image = request.FILES['image']
                profile.save()
                return redirect('profile_Interno')  # Redirigir a la misma vista o la que prefieras
            except Exception as e:
                logger.error(f"Error saving profile interno: {str(e)}")
    else:
        form = ProfileForm(instance=request.user.profile)

    return render(request, 'profileInterno.html', {'form': form})




@login_required
def reportarEmergencia(request):
    if request.method == 'POST':
        descripcion = request.POST.get('descripcion')
        ubicacion = request.POST.get('location')
        
        # Crea una emergencia asociada al usuario logueado
        Emergencias.objects.create(
            user=request.user,  # Asociar la emergencia al usuario que hizo el reporte
            descripcion=descripcion,
            ubicacion=ubicacion
        )
        
        messages.success(request, 'Reporte agregado correctamente')
        return redirect('reportEmergency')
    
    else:
        messages.error(request, 'Hubo un error en el reporte, intenta de nuevo')
        return redirect('reportEmergency')








# from django.core.files.storage import default_storage
# from django.core.files.base import ContentFile

# def test_s3_connection(request):
#     # Intenta crear un archivo de prueba en S3
#     path = default_storage.save('test-file.txt', ContentFile('Test content'))
#     # Intenta recuperar la URL del archivo
#     url = default_storage.url(path)
#     return HttpResponse(f"File saved at: {url}")


# def prueba(request):
#     return (request, 'prueba.html')