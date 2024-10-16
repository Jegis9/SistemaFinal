from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models

class CV(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relacionar con el perfil de usuario
    cargo = models.CharField(max_length=100)
    sobre_mi = models.TextField(max_length=1000)
    tipo_sangre = models.CharField(max_length=10)
    contacto_telefono_emergencia = models.CharField(max_length=15, blank=True, null=True)
    contacto_email = models.EmailField(blank=True, null=True)
    habilidades = models.TextField(max_length=1000, blank=True)
    estado = models.CharField(max_length=100)

    def __str__(self):
        return f"CV de {self.user.username}"
class Experiencia(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name='experiencias')
    puesto = models.CharField(max_length=255)
    empresa = models.CharField(max_length=255)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return f"{self.puesto} en {self.empresa}"
class Certificado(models.Model):
    cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name='certificados')
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    url_archivo = models.URLField(max_length=500, help_text="Ingrese la URL del certificado (por ejemplo, Google Drive)")

    def __str__(self):
        return self.titulo
