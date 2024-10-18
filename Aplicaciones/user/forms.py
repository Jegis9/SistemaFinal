from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

# creacion de campos al momento de crear un nuevo perfil
# estos campos son para la creacion desde la pagina publica de los usuarios (falta guardar los extras)
# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    ROLES = (
        ('admin', 'Administrador'),
        ('staff', 'Personal'),
        ('public', 'Publico'),
    )
    
    role = forms.ChoiceField(
        choices=ROLES,
        required=False,
        label='Rol del usuario',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    pdi = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    name1 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    name2 = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    lastname1 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    lastname2 = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    birthday = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    municipio = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    direccion = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.RadioSelect,
        label="Género"
    )
    is_internal = forms.BooleanField(
        required=False,
        widget=forms.HiddenInput(),
        initial=True
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role', 'pdi', 
                 'name1', 'name2', 'lastname1', 'lastname2', 'birthday', 
                 'phone', 'municipio', 'direccion', 'gender', 'is_internal']
        
        
from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['pdi', 'name1', 'name2', 'lastname1', 'lastname2', 'birthday', 'phone', 'municipio', 'direccion', 'gender',  'image']
