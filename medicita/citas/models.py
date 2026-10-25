from datetime import time
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q

class Especialidad(models.Model):
    nombre = models.CharField(max_length=80)
    def __str__(self): return self.nombre

class Centro(models.Model):
    nombre = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=60)
    direccion = models.CharField(max_length=150)
    def __str__(self): return f"{self.nombre} ({self.ciudad})"

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20, blank=True)
    ciudad = models.CharField(max_length=60, blank=True)
    barrio = models.CharField(max_length=80, blank=True)
    expediente = models.TextField("Expediente / antecedentes", blank=True)
    def __str__(self): return self.user.username

class Medico(models.Model):
    nombre = models.CharField(max_length=100)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.PROTECT)
    centro = models.ForeignKey(Centro, on_delete=models.PROTECT)
    hora_inicio = models.TimeField(default=time(8, 0))
    hora_fin = models.TimeField(default=time(17, 0))
    duracion = models.PositiveIntegerField("Minutos por cita", default=30)
    def __str__(self): return self.nombre

class Cita(models.Model):
    ESTADOS = [("programada", "Programada"), ("cancelada", "Cancelada")]
    paciente = models.ForeignKey(User, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField()
    motivo = models.CharField(max_length=200, blank=True)
    estado = models.CharField(max_length=12, choices=ESTADOS, default="programada")
    creada_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="+")
    class Meta:
        constraints = [models.UniqueConstraint(fields=["medico", "fecha_hora"],
            condition=Q(estado="programada"), name="sin_cruce_medico")]
