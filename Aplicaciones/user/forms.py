from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

# creacion de campos al momento de crear un nuevo perfil
# estos campos son para la creacion desde la pagina publica de los usuarios (falta guardar los extras)
class CreateUserForm(UserCreationForm):
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    
    email = forms.EmailField()
    pdi = forms.IntegerField(required=False)  # Make it optional
    name1 = forms.CharField()
    name2 = forms.CharField(required=False)
    lastname1 = forms.CharField()
    lastname2 = forms.CharField(required=False)
    birthday = forms.DateField()  # Fixed spelling
    phone = forms.CharField(max_length=15, required=False)  # Changed to CharField
    municipio = forms.CharField(required=False)
    direccion = forms.CharField(required=False)
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.RadioSelect,
        label="Gender"
    )
    is_internal = forms.BooleanField(required=False, widget=forms.HiddenInput(), initial=False)

# se envian los campos agregados para que aparezcan en el formulario del sistema y que cuando se llame al formulario desde login.html 
# se cree el registro llenando todos los campos
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
        
