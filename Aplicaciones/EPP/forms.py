from django import forms
from .models import PersonalEpps
from .models import Epp
class AsignacionEppForm(forms.ModelForm):
    class Meta:
        model = PersonalEpps
        fields = ['idPersonal', 'idEpp']
        widgets = {
            'idPersonal': forms.Select(attrs={'class': 'form-control'}),
            'idEpp': forms.Select(attrs={'class': 'form-control'}),
        }



class EPPForm(forms.ModelForm):
    class Meta:
        model = Epp
        fields = ['codigo', 'nombre']  # Asegúrate de incluir todos los campos necesarios
