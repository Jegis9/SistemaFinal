from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.utils import timezone

class Herramienta(models.Model):
    codigo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre
class MantenimientoHerramienta(models.Model):
    codigo = models.AutoField(primary_key=True)
    herramienta = models.ForeignKey(Herramienta, on_delete=models.CASCADE)
    reportado = models.DateTimeField(default=timezone.now)
    descripcion = models.CharField(max_length=255)  # Mayor longitud
    tiempo_mantenimiento = models.DateField()

class EstadoHerramienta(models.Model):
    codigo = models.AutoField(primary_key=True)
    herramienta = models.ForeignKey(Herramienta, on_delete=models.CASCADE)
    reportado = models.DateTimeField(default=timezone.now)
    descripcion = models.CharField(max_length=255)  # Mayor longitud
    estado = models.CharField(default='bueno',max_length=100)