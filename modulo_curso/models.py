from django.db import models
from django.core.exceptions import ValidationError
from modulo_docente.models import docente

# Create your models here.
from django.db import models

# Create your models here.

class facultad(models.Model):
    nombre_facultad = models.CharField(max_length=100)
    responsable_facultad = models.CharField(max_length=100, default='Sin responsable')

    def __str__(self):
        return self.nombre_facultad
    
    class Meta:
        verbose_name_plural="Facultad"

class escuela(models.Model):
    nombre_escuela = models.CharField(max_length=60)
    director_escuela = models.CharField(max_length=60, default='Sin director')
    fk_facultad = models.ForeignKey(facultad, on_delete=models.CASCADE,default=None) 

    def __str__(self):
        return self.nombre_escuela
    
    class Meta:
        verbose_name_plural="Escuela"
    
class tipo_curso(models.Model):
    tipo_curso = models.CharField(max_length=100, default='Curso presencial')
    descripcion_curso = models.CharField(max_length=50)

    def __str__(self):
        return self.tipo_curso
    
    class Meta:
        verbose_name_plural="Tipo de curso"

class plan_estudio(models.Model):
    plan_nombre = models.CharField(max_length=60, default='plan 2024')
    plan_descripcion = models.CharField(max_length=60)
    plan_fechacreacion =models.DateField()
    fk_escuela = models.ForeignKey(escuela, on_delete=models.CASCADE, default=None)
    plan_estado = models.BooleanField(default=True)

    def __str__(self):
        return self.plan_nombre
    
    class Meta:
        verbose_name_plural="Plan de estudio"

class curso(models.Model):
    codigo_curso = models.CharField(max_length=20,unique=True)
    nombre_curso = models.CharField(max_length=100)
    horas_totales = models.SmallIntegerField(default=1)
    horas_practicas = models.SmallIntegerField(default=1) 
    horas_teoricas = models.SmallIntegerField(default=1)
    ciclo_curso = models.SmallIntegerField(default=1)
    amb = models.SmallIntegerField(default=1)
    FKtipocurso = models.ForeignKey(tipo_curso, on_delete=models.CASCADE) 
    FKplan_estudio = models.ForeignKey(plan_estudio, on_delete=models.CASCADE, default=None)
    def Validacion_horas(self):
        if self.horas_practicas + self.horas_teoricas != self.horas_totales:
            raise ValidationError("La suma de las horas prácticas y teóricas debe ser igual a las horas totales.")
    
    def __str__(self):
        return self.nombre_curso
    
    class Meta:
        verbose_name_plural="Curso"

