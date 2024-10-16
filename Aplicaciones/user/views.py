from django.shortcuts import render, redirect
# importar libreria para el registro de usuarios
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .models import Profile
from django.contrib.auth import logout
# Create your views here.

# crear vista para que redirija a index que es la pagina principal
def landingPage(request):
    return render(request, 'index.html')

# crear vista para que redirija a index que es la pagina de registrar usuario
def register(request):
    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return render(request, 'logout_sale.html')




# # crear formulario generado por django para registro de usuarios 
def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            try:
                profile = user.profile
            except Profile.DoesNotExist:
                profile = Profile(user=user)
            
            profile.is_internal = False
            profile.pdi = form.cleaned_data.get('pdi')
            profile.name1 = form.cleaned_data['name1']
            profile.name2 = form.cleaned_data.get('name2', '')
            profile.lastname1 = form.cleaned_data['lastname1']
            profile.lastname2 = form.cleaned_data.get('lastname2', '')
            profile.birthday = form.cleaned_data['birthday']  # Fixed spelling
            profile.phone = form.cleaned_data.get('phone', '')
            profile.municipio = form.cleaned_data.get('municipio', '')
            profile.direccion = form.cleaned_data.get('direccion', '')
            profile.gender = form.cleaned_data['gender']
            profile.save()
            
            messages.success(request, 'Nuevo usuario agregado correctamente')
        else:
            print("Errores del formulario:", form.errors)
            print("Datos recibidos:", request.POST)
    else:
        form = CreateUserForm()
    
    context = {'form': form}
    return render(request, 'register.html', context)

def nuevo_registro(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            try:
                profile = user.profile
            except Profile.DoesNotExist:
                profile = Profile(user=user)
            
            profile.is_internal = True
            profile.pdi = form.cleaned_data.get('pdi')
            profile.name1 = form.cleaned_data['name1']
            profile.name2 = form.cleaned_data.get('name2', '')
            profile.lastname1 = form.cleaned_data['lastname1']
            profile.lastname2 = form.cleaned_data.get('lastname2', '')
            profile.birthday = form.cleaned_data['birthday']  # Fixed spelling
            profile.phone = form.cleaned_data.get('phone', '')
            profile.municipio = form.cleaned_data.get('municipio', '')
            profile.direccion = form.cleaned_data.get('direccion', '')
            profile.gender = form.cleaned_data['gender']
            profile.save()
            
            messages.success(request, 'Nuevo usuario agregado correctamente')
            return redirect('lInternos')
        else:
            print("Errores del formulario:", form.errors)
    
    else:
        form = CreateUserForm()
    
    context = {'formulario': form}
    return render(request, 'registerInternal.html', context)








class CustomLoginView(View):    # creamos esta nueva vista para modificar el formulario de login por defecto de django
    def get(self, request): 
        form = AuthenticationForm() # por lo que solicitamos (GET carga la pagina) el formuario de django para autenticacion
        return render(request, 'login.html', {'form': form}) # y lo retornamos en la vista login.html donde se debera de mostrar el formato

    def post(self, request): # si el formulario es (POST envio de datos)
        form = AuthenticationForm(data=request.POST)
        if form.is_valid(): # verifica si el formulario es valido para poder iniciar sesion
            user = form.get_user() # si el usuario existe (previamente registrado)
            login(request, user)  # se inicia sesión con ese usuario
            # y se obtiene el perfil del usuario autenticado quien hizo la peticion el login
            profile = user.profile  # esto obtiene el perfil relacionado con el usuario

            # Redirige segun el valor de is_internal en el perfil relacionado con el usuario que inicia sesion
            if profile.is_internal:
                return redirect('estadisticas')  # Si es is_internal redirige a home (adminsitracion de la estacion)
            else:
                return redirect('reportEmergency')  # Si no es is_internal redirige a reportEmergency (acceso a personas agenas a la estacion)
        return render(request, 'login.html', {'form': form}) # aqui renderiza el formulario dende se cargara el formulario djanfo para el login












