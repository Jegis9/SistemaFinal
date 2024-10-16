from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
# creacion de campos al momento de crear un nuevo perfil
# estos campos son para la creacion desde la pagina publica de los usuarios (falta guardar los extras)
class CustomCreateUserForm(UserCreationForm):

    # se agrega este campo para poder verificar y crear el perfil del usuario relacionado
    is_internal = forms.BooleanField(required=False, widget=forms.HiddenInput(), initial=True)
# se envian los campos agregados para que aparezcan en el formulario del sistema y que cuando se llame al formulario desde login.html 
# se cree el registro llenando todos los campos
    class Meta: 
        model = User
        fields = ['username','password1','password2','is_internal']
        