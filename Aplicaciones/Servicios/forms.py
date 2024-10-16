# your_app/forms.py

from django import forms
from .models import ServicioPrincipal

class ServicioForm(forms.ModelForm):
    class Meta:
        model = ServicioPrincipal
        fields = '__all__'
        widgets = {
            'fecha_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'salida_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'entrada_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'hora_efectiva': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
