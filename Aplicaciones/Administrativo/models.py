from django.db import models
from django.utils import timezone
# Create your models here.

# modelo de insumos

class Insumos(models.Model):
    codigo=models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    stock_inicial = models.IntegerField(default=0)
    stock_actual = models.IntegerField(default=0)
 
    
# mostrar el contenido del insumo 
    def __str__(self):
        texto = "{0} ({1})"
        return texto.format(self.nombre, self.stock_inicial, self.stock_actual)
    
    
# modelo para crear el log de insumos

class InsumoLog(models.Model):
    insumo = models.ForeignKey('Insumos', on_delete=models.CASCADE, related_name='logs')

    cantidadTomada = models.IntegerField()
    total = models.IntegerField()
    fecha_hora = models.DateTimeField(default=timezone.now)
 

    def __str__(self):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
        return f"{self.insumo.nombre} - {self.cantidadTomada} unidades - {self.total} -{self.fecha_hora}"



