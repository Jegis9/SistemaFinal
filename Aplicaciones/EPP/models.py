from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class Epp(models.Model):
    codigo=models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre
class PersonalEpps(models.Model):
    idPersonal = models.ForeignKey(User, on_delete=models.CASCADE)
    idEpp = models.ForeignKey(Epp, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre
class EstadoEPP(models.Model):
    codigo=models.AutoField(primary_key=True)
    PersonalEpps = models.ForeignKey(PersonalEpps, on_delete=models.CASCADE)
    reportado = models.DateTimeField(default=timezone.now)  # Valor por defecto para las filas existentes
    descripcion = models.CharField(null=False, blank=False, max_length=100)
    
    estado = models.CharField(default='malo',max_length=100)