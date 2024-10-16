from django import forms
from .models import CV, Certificado, Experiencia
from .models import Certificado
import requests
from django.core.exceptions import ValidationError
import re




class CVForm(forms.ModelForm):
    class Meta:
        model = CV
        fields = ['cargo', 'sobre_mi', 'tipo_sangre', 'contacto_telefono_emergencia', 'contacto_email', 'habilidades', 'estado']
        widgets = {
            'sobre_mi': forms.Textarea(attrs={'rows': 4}),
            'habilidades': forms.Textarea(attrs={'rows': 4}),
        }





from .models import Experiencia

class ExperienciaForm(forms.ModelForm):
    class Meta:
        model = Experiencia
        fields = ['puesto', 'empresa', 'fecha_inicio', 'fecha_fin', 'descripcion']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }




class CVForm(forms.ModelForm):
    class Meta:
        model = CV
        fields = ['cargo', 'sobre_mi', 'tipo_sangre', 'contacto_telefono_emergencia', 'contacto_email', 'habilidades', 'estado']
        widgets = {
            'sobre_mi': forms.Textarea(attrs={'rows': 4}),
            'habilidades': forms.Textarea(attrs={'rows': 4}),
        }

class ExperienciaForm(forms.ModelForm):
    class Meta:
        model = Experiencia
        fields = ['puesto', 'empresa', 'fecha_inicio', 'fecha_fin', 'descripcion']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }


def extract_file_id(url):
    # Patrón para extraer el ID del archivo de Google Drive
    pattern = r'/d/([a-zA-Z0-9_-]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

def validate_pdf_url(url):
    try:
        file_id = extract_file_id(url)
        if not file_id:
            raise ValidationError('No se pudo extraer el ID del archivo de Google Drive.')
        
        # Construir la URL de descarga directa
        direct_url = f'https://drive.google.com/uc?id={file_id}'
        
        # Realizar una solicitud HEAD a la URL directa
        response = requests.head(direct_url, allow_redirects=True)
        
        # Verificar si la respuesta es exitosa
        if response.status_code != 200:
            raise ValidationError('No se pudo acceder al archivo en Google Drive.')
        
        # Intentar obtener el nombre del archivo de las cabeceras
        content_disposition = response.headers.get('Content-Disposition', '')
        if 'pdf' not in content_disposition.lower():
            # Si no podemos confirmar que es un PDF por las cabeceras,
            # podríamos hacer una solicitud GET parcial para verificar el contenido
            response = requests.get(direct_url, stream=True)
            content = next(response.iter_content(256))
            
            # Verificar la firma de archivo PDF (%PDF-)
            if not content.startswith(b'%PDF-'):
                raise ValidationError('El archivo no parece ser un PDF válido.')
    
    except requests.RequestException:
        raise ValidationError('No se pudo acceder a la URL proporcionada.')

class CertificadoForm(forms.ModelForm):
    class Meta:
        model = Certificado
        fields = ['titulo', 'descripcion', 'url_archivo']
        widgets = {
            'url_archivo': forms.URLInput(attrs={'placeholder': 'https://drive.google.com/...'}),
        }
    
    def clean_url_archivo(self):
        url = self.cleaned_data.get('url_archivo')
        
        # Verificar que la URL es de Google Drive
        if not ('drive.google.com' in url or 'docs.google.com' in url):
            raise ValidationError('Solo se permiten URLs de Google Drive.')
        
        # Validar que la URL apunte a un archivo PDF válido
        validate_pdf_url(url)
        return url