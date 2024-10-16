# # your_app/models.py

# from django.db import models

# class ServicioPrincipal(models.Model):
#     SERVICIO_CHOICES = [
#         ('Varios', 'Varios'),
#         ('Ambulancia', 'Ambulancia'),
#         ('Incendios', 'Incendios'),
#     ]

#     direccion = models.CharField(max_length=255)
#     kmEntrada = models.DecimalField(max_digits=10, decimal_places=2)
#     kmSalida = models.DecimalField(max_digits=10, decimal_places=2)
#     jefeServicio = models.CharField(max_length=100)
    
#     bomberoReporta = models.CharField(max_length=100)
    
#     fecha_hora = models.DateTimeField()
#     salida_hora = models.DateTimeField()
#     entrada_hora = models.DateTimeField()
#     servicio = models.CharField(max_length=20, choices=SERVICIO_CHOICES)
#     observaciones = models.TextField(blank=True, null=True)
#     turno = models.CharField(max_length=50)
#     telefonista = models.CharField(max_length=100)
#     # Campos específicos para "Varios"
#     tipo_servicio_varios = models.CharField(max_length=100, blank=True, null=True)
#     autorizado_por = models.CharField(max_length=100, blank=True, null=True)

#     # Campos específicos para "Ambulancia"
#     direccion_traslado = models.CharField(max_length=255, blank=True, null=True)
#     nombre_paciente = models.CharField(max_length=100, blank=True, null=True)
#     direccion_paciente = models.CharField(max_length=255, blank=True, null=True)
#     edad = models.PositiveIntegerField(blank=True, null=True)
#     sexo = models.CharField(max_length=10, blank=True, null=True)
#     traslado_A = models.CharField(max_length=100, blank=True, null=True)
#     forma_aviso = models.CharField(max_length=100, blank=True, null=True)

#     # Campos específicos para "Incendios"
#     servicio_incendio_inmueble = models.CharField(max_length=255, blank=True, null=True)
#     valor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     perdida = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     proporcion = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
#     clase_fuego = models.CharField(max_length=50, blank=True, null=True)
#     hora_efectiva = models.DateTimeField(blank=True, null=True)

#     def __str__(self):
#         return f"{self.servicio} - {self.fecha_hora}"
