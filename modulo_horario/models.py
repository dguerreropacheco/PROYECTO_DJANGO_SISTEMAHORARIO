from django.db import models
from modulo_curso.models import curso, escuela
from modulo_docente.models import docente
from modulo_ambiente.models import ambiente


# Create your models here.
class dia_semana(models.Model):
    dia_nombre = models.CharField(max_length=9)
    estado = models.BooleanField(default=False)

    def __str__(self):
        return self.dia_nombre

    class Meta:
        verbose_name_plural="Día de la semana"

class ciclo_academico(models.Model):
    cic_año = models.CharField(max_length=4)
    cic_semestre = models.CharField(max_length=7)

    def __str__(self):
        return self.cic_año + ' - ' + self.cic_semestre

    class Meta:
        verbose_name_plural="Ciclo académico"


class grupo_horario(models.Model):
    grupo = models.CharField(max_length=1)
    capacidad = models.PositiveSmallIntegerField(default=15)
    fk_ciclo = models.ForeignKey(ciclo_academico, on_delete=models.CASCADE, default=None)
    fk_curso = models.ForeignKey(curso, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.grupo
    
    class Meta:
        verbose_name_plural="Grupo Horario"

class horario (models.Model):
    hora_de_inicio = models.CharField(max_length=5,default='00:00', verbose_name="Hora de inicio")
    hora_final = models.CharField(max_length=5, default='00:00')
    motivo_cambio = models.CharField(max_length=150,null=True,blank=True)
    ambiente = models.ForeignKey(ambiente, blank=True,null=False,on_delete=models.CASCADE)
    día = models.ForeignKey(dia_semana, blank=True,null=False,on_delete=models.CASCADE, verbose_name="Día")
    fk_grupo_horario = models.ForeignKey(grupo_horario, blank=True,null=False,on_delete=models.CASCADE, verbose_name="Curso")

    def __str__(self):
        return str(self.día) +'- '+ str(self.hora_de_inicio) +'- '+ str(self.hora_final)


    class Meta:
        verbose_name_plural="Horario"

class escuela_ambiente(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion= models.CharField
    FK_escuela  = models.ForeignKey(escuela, on_delete=models.CASCADE, verbose_name='Escuela')
    FK_ambiente  = models.ForeignKey(ambiente, on_delete=models.CASCADE, verbose_name='Ambiente')
    FK_ciclo_academico = models.ForeignKey(ciclo_academico, on_delete=models.CASCADE, verbose_name='ciclo')