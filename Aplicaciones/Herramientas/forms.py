from django import forms
from .models import Herramienta, MantenimientoHerramienta


class HerramientasForm(forms.ModelForm):
    class Meta:
        model = Herramienta
        fields = ['codigo', 'nombre']  # Asegúrate de incluir todos los campos necesarios
        
        
        
class MantenimientoForm(forms.ModelForm):
    class Meta:
        model = MantenimientoHerramienta
        fields = ['codigo', 'herramienta','descripcion','tiempo_mantenimiento']  # Asegúrate de incluir todos los campos necesarios
         
        
  