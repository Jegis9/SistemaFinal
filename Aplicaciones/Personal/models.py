from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Modelo del personal
class Personal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relacionar con el perfil de usuario
  
    cargo = models.CharField(max_length=100, null=False, blank=False)
    sobre_mi = models.CharField(max_length=100, null=False, blank=False)
    tipo_sangre = models.CharField(max_length=10, null=False, blank=False)
    contacto_telefono_emergencia = models.CharField(max_length=15, blank=True, null=True)
    contacto_email = models.EmailField(blank=True, null=True)
    habilidades = models.ManyToManyField('Habilidad')  # Relación muchos a muchos
    certificaciones = models.ManyToManyField('Certificacion')  # Relación muchos a muchos
    estado = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.cargo}"

# Modelo de experiencia laboral
class Experiencia(models.Model):
    personal = models.ForeignKey(Personal, on_delete=models.CASCADE, related_name='experiencias')  # Relación uno a muchos
    descripcion = models.CharField(max_length=200, null=False, blank=False)
    fecha_inicio = models.DateField(null=False, blank=False)
    fecha_fin = models.DateField(null=False, blank=False)
    cargo = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return f"{self.cargo} en {self.descripcion}"

# Modelo de certificaciones
class Certificacion(models.Model):
    nombre = models.CharField(max_length=100, null=False, blank=False)
    institucion = models.CharField(max_length=100, null=False, blank=False)
    fecha_inicio = models.DateField(null=False, blank=False)
    fecha_fin = models.DateField(null=False, blank=False)

    def __str__(self):
        return self.nombre

# Modelo de habilidades
class Habilidad(models.Model):
    nombre = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.nombre

# Modelo de educación
class Educacion(models.Model):
    personal = models.ForeignKey(Personal, on_delete=models.CASCADE, related_name='educaciones')  # Relación uno a muchos
    titulo = models.CharField(max_length=100, null=False, blank=False)
    institucion = models.CharField(max_length=100, null=False, blank=False)
    fecha_inicio = models.DateField(null=False, blank=False)
    fecha_fin = models.DateField(null=False, blank=False)

    def __str__(self):
        return f"{self.titulo} - {self.institucion}"
