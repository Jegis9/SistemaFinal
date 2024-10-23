

# your_app/forms.py

from django import forms
from .models import Servicio, Varios, Ambulancia, Incendios, Categorias_emergencias

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = [
            'estacion', 'turno', 'direccion', 'telefonista', 'bombero_reporta',
            'unidad', 'piloto', 'salida_hora', 'entrada_hora',
            'personal_asistente', 'fecha_hora', 'km_entrada', 'km_salida',
            'km_recorridos', 'servicio', 'observaciones'
        ]
        widgets = {
            'fecha_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'salida_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'entrada_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'servicio': forms.RadioSelect,  # Renderizar como botones de radio
        }

class VariosForm(forms.ModelForm):
    servicio_de = forms.CharField(
        max_length=100, 
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Servicio De'})
    )
    jefe_servicio = forms.CharField(
        max_length=100, 
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Jefe de Servicio'})
    )
    servicio_autorizado_por = forms.CharField(
        max_length=100, 
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Servicio Autorizado Por'})
    )
    fecha = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    class Meta:
        model = Varios
        fields = ['fecha', 'servicio_de', 'jefe_servicio', 'servicio_autorizado_por']

class AmbulanciaForm(forms.ModelForm):
    codigo_emergencia = forms.ModelChoiceField(
        queryset=Categorias_emergencias.objects.all(),
        required=False,
        widget=forms.Select(attrs={'placeholder': 'Código de Emergencia'})
    )
    nombre_paciente = forms.CharField(
        max_length=100, 
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Nombre del Paciente'})
    )
    direccion_paciente = forms.CharField(
        max_length=255, 
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Dirección del Paciente'})
    )
    edad = forms.IntegerField(
        min_value=0, 
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Edad'})
    )
    sexo = forms.ChoiceField(
        choices=[
            ('F', 'Femenino'),
            ('M', 'Masculino'),
        ],
        required=False,
        widget=forms.Select()
    )
    traslado_a = forms.CharField(
        max_length=100, 
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Traslado A'})
    )
    forma_aviso = forms.CharField(
        max_length=100, 
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Forma de Aviso'})
    )
    hora_efectiva_servicio = forms.TimeField(
        required=False,
        widget=forms.TimeInput(attrs={'type': 'time'})
    )

    class Meta:
        model = Ambulancia
        fields = [
            'codigo_emergencia', 'nombre_paciente', 'direccion_paciente',
            'edad', 'sexo', 'traslado_a', 'forma_aviso', 'hora_efectiva_servicio'
        ]

class IncendiosForm(forms.ModelForm):
    servicio_incendio_inmueble = forms.CharField(
        max_length=255, 
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Servicio Incendio Inmueble'})
    )
    valor = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Valor'})
    )
    perdida = forms.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Pérdida'})
    )
    proporcion = forms.ChoiceField(
        choices=Incendios.PROPORCION_CHOICES,
        required=False,
        widget=forms.Select(attrs={'placeholder': 'Proporción'})
    )
    clase_fuego = forms.ChoiceField(
        choices=Incendios.CLASE_FUEGO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'placeholder': 'Clase de Fuego'})
    )
    hora_efectiva = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    otras_unidades_asistentes_estacion = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Otras Unidades Asistentes en Estación'})
    )
    unidades_asistentes_otras_estaciones = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Unidades Asistentes en Otras Estaciones'})
    )
    unidades_policiacas = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Unidades Policiacas'})
    )
    unidades_otras_instituciones_bomberiles = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Unidades de Otras Instituciones Bomberiles'})
    )
    personal_asistente_otras_estaciones = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Personal Asistente en Otras Estaciones'})
    )
    fecha = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Incendios
        fields = [
            'servicio_incendio_inmueble', 'valor', 'perdida',
            'proporcion', 'clase_fuego', 'hora_efectiva',
            'otras_unidades_asistentes_estacion',
            'unidades_asistentes_otras_estaciones',
            'unidades_policiacas',
            'unidades_otras_instituciones_bomberiles',
            'personal_asistente_otras_estaciones',
            'fecha'
        ]
        
class CategoriasEmergenciasForm(forms.ModelForm):
    class Meta:
        model = Categorias_emergencias
        fields = ['id', 'nombre']