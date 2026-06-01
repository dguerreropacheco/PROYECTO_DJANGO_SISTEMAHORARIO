from django.db import models

# Create your models here.
class departamento_academico(models.Model):
    dep_nombre = models.CharField(max_length=50)
    dep_director = models.CharField(max_length=100)	

    def __str__(self):
        return self.dep_nombre   
    
    class Meta:
        verbose_name_plural="Departamento académico"


class tipo_contrato(models.Model):
    tp_nombre = models.CharField(max_length=50)
    tp_descripcion = models.CharField(max_length=100)
    tp_horas = models.SmallIntegerField()

    def __str__(self):
        return self.tp_nombre
    
    class Meta:
        verbose_name_plural="Tipo de contrato"

class docente(models.Model):
    
    doc_nombres = models.CharField(max_length=200)
    doc_especialidad = models.CharField(max_length=100)
    doc_email = models.CharField(max_length=50)
    doc_estado = models.CharField(max_length=10) 
    doc_telefono = models.CharField(max_length=9)
    FKtipocontrato = models.ForeignKey (tipo_contrato, on_delete=models.CASCADE)
    FKdepartamentoacademico = models.ForeignKey(departamento_academico, on_delete=models.CASCADE)

    def __str__(self):
        return self.doc_nombres 
    
    class Meta:
        verbose_name_plural="Docente"
    
class disponibilidad_docente(models.Model):
    id = models.AutoField(primary_key=True)
    ddo_horainicio = models.TimeField()
    ddo_horafin = models.TimeField()
    FKdiasemana = models.ForeignKey('modulo_horario.dia_semana', on_delete=models.CASCADE)
    FKdocente = models.ForeignKey(docente, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.FKdocente) + ' - ' + str(self.FKdiasemana) + ' '+ str(self.ddo_horainicio)+ '-' + str(self.ddo_horafin)
    
    class Meta:
        verbose_name_plural="Disponibilidad docente"
        ordering=['FKdocente']


class docente_grupo(models.Model):
     id = models.AutoField(primary_key=True)
     FKgrupo = models.ForeignKey('modulo_horario.grupo_horario', on_delete=models.CASCADE)
     FKdocente = models.ForeignKey(docente, on_delete=models.CASCADE)

     def __str__(self):
         return str(self.id)
    
     class Meta:
         verbose_name_plural="Docente grupo"
         ordering=['id']