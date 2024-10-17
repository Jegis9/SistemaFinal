# your_app/models.py

from django.db import models

class Servicio(models.Model):
    SERVICIO_CHOICES = [
        ('1', 'Varios'),
        ('2', 'Ambulancia'),
        ('3', 'Incendios'),
    ]
    estacion = models.CharField(max_length=50)
    turno = models.CharField(max_length=50)
    direccion = models.CharField(max_length=255)
    telefonista = models.CharField(max_length=100)
    bombero_reporta = models.CharField(max_length=100)
    unidad = models.CharField(max_length=50)
    piloto = models.CharField(max_length=50)
    salida_hora = models.DateTimeField()
    entrada_hora = models.DateTimeField()
    personal_asistente = models.CharField(max_length=100)
    observaciones = models.TextField()  # Cambiado a TextField
    km_entrada = models.DecimalField(max_digits=10, decimal_places=2)
    km_salida = models.DecimalField(max_digits=10, decimal_places=2)
    km_recorridos = models.FloatField()
    servicio = models.CharField(max_length=50, choices=SERVICIO_CHOICES)  # Añadido
    fecha_hora = models.DateTimeField(db_index=True)  # Añadido
    activo = models.BooleanField(default=True)  # Campo para desactivación lógica
    def __str__(self):
        return f"{self.servicio} - {self.fecha_hora}"


class Varios(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='varios')

    fecha = models.DateField()
    servicio_de = models.CharField(max_length=100)
    jefe_servicio = models.CharField(max_length=100)
    servicio_autorizado_por = models.CharField(max_length=100)

    def __str__(self):
        return f"Varios - {self.servicio}"

class Categorias_emergencias(models.Model):
    id = models.CharField(primary_key=True, max_length=10)  # Sobrescribe el campo id
    nombre = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.nombre


class Ambulancia(models.Model):

    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='ambulancia')
    codigo_emergencia = models.ForeignKey(Categorias_emergencias, on_delete=models.CASCADE, related_name='Categorias', null=True, blank=True)
    nombre_paciente = models.CharField(max_length=100)
    direccion_paciente = models.CharField(max_length=255)
    edad = models.PositiveIntegerField()
    sexo = models.CharField(max_length=10, choices=[
        ('F', 'Femenino'),
        ('M', 'Masculino'),
    ])
    traslado_a = models.CharField(max_length=100)  
    forma_aviso = models.CharField(max_length=100)
    hora_efectiva_servicio = models.TimeField()

    def __str__(self):
        return f"Ambulancia - {self.servicio}"


class Incendios(models.Model):
    PROPORCION_CHOICES = [
        ('Declarado', 'Declarado'),
        ('Medio', 'Medio'),
        ('Conato', 'Conato'),
    ]

    CLASE_FUEGO_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ]

    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='incendios')
    servicio_incendio_inmueble = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    perdida = models.DecimalField(max_digits=10, decimal_places=2)
    proporcion = models.CharField(max_length=10, choices=PROPORCION_CHOICES)  # Cambiado a CharField
    clase_fuego = models.CharField(max_length=1, choices=CLASE_FUEGO_CHOICES)  # max_length ajustado
    hora_efectiva = models.DateTimeField()
    otras_unidades_asistentes_estacion = models.CharField(max_length=255)
    unidades_asistentes_otras_estaciones = models.CharField(max_length=255)
    unidades_policiacas = models.CharField(max_length=255)
    unidades_otras_instituciones_bomberiles = models.CharField(max_length=255)
    personal_asistente_otras_estaciones = models.CharField(max_length=255)
    jefe_servicio = models.CharField(max_length=100)
    fecha = models.DateField()

    def __str__(self):
        return f"Incendios - {self.servicio}"
