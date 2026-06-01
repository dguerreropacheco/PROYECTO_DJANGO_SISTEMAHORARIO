from django.db import models
from modulo_curso.models import *

# Create your models here.
class edificio( models.Model):
    nombre_edificio = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_edificio
    
    class Meta:
        verbose_name_plural="Edificio"


class tipo_ambiente(models.Model):
    tipo_de_ambiente = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=50)

    def __str__(self):
        return self.tipo_de_ambiente
    
    class Meta:
        verbose_name_plural="Tipo de ambiente"
    
    
class ambiente(models.Model):
    nombre_ambiente = models.CharField(max_length=30)
    capacidad_ambiente = models.PositiveSmallIntegerField(default=15)
    estado_ambiente = models.CharField(max_length=1, choices=(('D', 'Disponible'), ('O', 'Ocupado'),('M', 'Mantenimiento')))
    piso = models.PositiveSmallIntegerField(default=1)
    FKedificio  = models.ForeignKey(edificio, on_delete=models.CASCADE, verbose_name='Edificio')
    FKtipo_ambiente = models.ForeignKey(tipo_ambiente, on_delete=models.CASCADE, verbose_name='Tipo de Ambiente')

    def __str__(self):
        return self.nombre_ambiente + '(' + str(self.capacidad_ambiente) + ')'
    
    class Meta:
        verbose_name_plural="Ambiente"

   

