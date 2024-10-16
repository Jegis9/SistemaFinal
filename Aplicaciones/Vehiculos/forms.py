from django import forms
from .models import Vehiculos

class VEHForm(forms.ModelForm):
    class Meta:
        model = Vehiculos
        fields = [ 'placas', 'tipo_vehiculo']  # Asegúrate de incluir todos los campos necesarios
