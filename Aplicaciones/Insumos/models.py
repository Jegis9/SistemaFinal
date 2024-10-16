from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Insumo(models.Model):
    codigo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    stock_inicial = models.IntegerField()
    stock_actual = models.IntegerField()
    
    def __str__(self):
        return f"{self.nombre} - Stock actual: {self.stock_actual}"

class MovimientoInsumo(models.Model):
    TIPO_MOVIMIENTO = [
        ('ENTRADA', 'Entrada'),
        ('SALIDA', 'Salida'),
    ]
    
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    idPersonal = models.ForeignKey(User, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    tipo_movimiento = models.CharField(max_length=7, choices=TIPO_MOVIMIENTO)
    fecha = models.DateTimeField(auto_now_add=True)
    observacion = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.tipo_movimiento} de {self.cantidad} - {self.insumo.nombre}"

 