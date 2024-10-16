from django import forms
from django.core.exceptions import ValidationError
from Aplicaciones.user.models import Profile
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']  # Esto servira para poder actualizar unicamente la imagen, se importa el modelo Profile y este campo es el unico que se puede actualizar en el perfil
        
    # Validación del archivo de imagen
    def clean_image(self):
        image = self.cleaned_data.get('image') # se pretende "limpiar" la iamgen subida que en realidad es una verificacion para que no se suba cualquier imagen

        if image:
            # 1. Validar que el archivo es una imagen JPG o JPEG
            if not image.name.lower().endswith(('.jpg', '.jpeg')):
                raise ValidationError('Solo se permiten imágenes en formato JPG o JPEG.') # mensaje de error si no cumple con el gormato, despues se llama en el htmlsi sucede

            # 2. Validar el tamaño del archivo (por ejemplo, no mayor a 2MB)
            max_size = 2 * 1024 * 1024  # 2 MB
            if image.size > max_size:
                raise ValidationError(f'El tamaño máximo de la imagen es de 2MB. El archivo subido tiene {image.size / 1024 / 1024:.2f}MB.')# mensaje de error si no cumple con el gormato, despues se llama en el htmlsi sucede

        return image