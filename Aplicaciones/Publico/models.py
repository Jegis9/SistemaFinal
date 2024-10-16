from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.



class Emergencias(models.Model):
    codigo = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=100)
    reportado = models.DateTimeField(default=timezone.now)  # Valor por defecto para las filas existentes
    atendido = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Emergencia {self.codigo} - {self.descripcion}'

      
      
      

    
    