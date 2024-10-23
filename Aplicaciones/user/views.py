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
# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from .models import Profile


def error(request):
    return render(request,'error.html')

# Funciones auxiliares para verificar permisos
def is_admin(user):
    return user.groups.filter(name='Administrador').exists()

def is_staff(user):
    return user.groups.filter(name='Personal').exists()


# crear vista para que redirija a index que es la pagina principal
def landingPage(request):
    return render(request, 'index.html')

# crear vista para que redirija a index que es la pagina de registrar usuario
def register(request):
    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return render(request, 'logout_sale.html')

from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile
from .forms import ProfileForm

def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_Interno')  # Redirige a una página de perfil o cualquier página que prefieras
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})


def edit_profile_externo(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirige a una página de perfil o cualquier página que prefieras
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'editar_profile_externo.html', {'form': form})



# # crear formulario generado por django para registro de usuarios 
def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            try:
                # Crear usuario
                user = form.save(commit=False)
                user.email = form.cleaned_data['email']
                user.save()

                # Asignar rol
                # Asignar rol
                # role = form.cleaned_data.get('role', 'public')  # Valor por defecto "public"
                # group_name = 'Administrador' if role == 'admin' else 'Personal' if role == 'staff' else 'Publico'
                # group = Group.objects.get(name=group_name)
                # user.groups.add(group)


                # Crear perfil
                profile = Profile(
                    user=user,
                    is_internal=False,
                    pdi=form.cleaned_data.get('pdi'),
                    name1=form.cleaned_data['name1'],
                    name2=form.cleaned_data.get('name2', ''),
                    lastname1=form.cleaned_data['lastname1'],
                    lastname2=form.cleaned_data.get('lastname2', ''),
                    birthday=form.cleaned_data['birthday'],
                    phone=form.cleaned_data.get('phone', ''),
                    municipio=form.cleaned_data.get('municipio', ''),
                    direccion=form.cleaned_data.get('direccion', ''),
                    gender=form.cleaned_data['gender']
                )
                profile.save()

                messages.success(request, 'Nuevo usuario agregado correctamente')
                return redirect('login')
            except Exception as e:
                messages.error(request, f'Error al crear el usuario: {str(e)}')
                print(f"Error detallado: {str(e)}")
        else:
            print("Errores del formulario:", form.errors)
            print("Datos recibidos:", request.POST)
    else:
        form = CreateUserForm()
    
    context = {'form': form}
    return render(request, 'register.html', context)


# Vista para crear usuarios (solo administradores)
# @login_required
# @user_passes_test(is_admin, login_url='error')

def nuevo_registro(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            try:
                # Crear usuario
                user = form.save(commit=False)
                user.email = form.cleaned_data['email']
                user.save()

                # Asignar rol
                role = form.cleaned_data.get('role')
                group = Group.objects.get(
                    name='Administrador' if role == 'admin' else 'Personal'
                )
                user.groups.add(group)

                # Crear perfil
                profile = Profile(
                    user=user,
                    is_internal=True,
                    pdi=form.cleaned_data.get('pdi'),
                    name1=form.cleaned_data['name1'],
                    name2=form.cleaned_data.get('name2', ''),
                    lastname1=form.cleaned_data['lastname1'],
                    lastname2=form.cleaned_data.get('lastname2', ''),
                    birthday=form.cleaned_data['birthday'],
                    phone=form.cleaned_data.get('phone', ''),
                    municipio=form.cleaned_data.get('municipio', ''),
                    direccion=form.cleaned_data.get('direccion', ''),
                    gender=form.cleaned_data['gender']
                )
                profile.save()

                messages.success(request, 'Nuevo usuario agregado correctamente')
                return redirect('lInternos')
            except Exception as e:
                messages.error(request, f'Error al crear el usuario: {str(e)}')
                print(f"Error detallado: {str(e)}")
        else:
            print("Errores del formulario:", form.errors)
            messages.error(request, 'Error en el formulario. Por favor, verifica los datos.')
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












