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


class Ambulancia(models.Model):
    EMERGENCY_CATEGORIES = [
        # A - Servicios de ambulancia
        ('A1.1', 'A - Servicios de ambulancia - 1. Heridos - 1.1 Arma de fuego'),
        ('A1.2', 'A - Servicios de ambulancia - 1. Heridos - 1.2 Arma blanca'),
        ('A2.1', 'A - Servicios de ambulancia - 2. Accidentes - 2.1 De tránsito'),
        ('A2.2', 'A - Servicios de ambulancia - 2. Accidentes - 2.2 Laborales'),
        ('A3.1', 'A - Servicios de ambulancia - 3. Atropellados - 3.1 Por vehículos no identificados'),
        ('A3.2', 'A - Servicios de ambulancia - 3. Atropellados - 3.2 Por vehículos livianos identificados'),
        
        # B - Rescates
        ('B17.1', 'B - Rescates - 17. Rescate de personas con vida - 17.1 Accidentes aéreos'),
        
        # Puedes seguir agregando más opciones aquí hasta la H
    ]
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='ambulancia')
    codigo_emergencia = models.CharField(
        max_length=10,
        choices=EMERGENCY_CATEGORIES,
        blank=True,
        help_text="Seleccione el tipo de emergencia",
        db_index=True
    )
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
