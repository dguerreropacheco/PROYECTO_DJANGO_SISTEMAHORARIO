from django.contrib import admin
from .models import docente, disponibilidad_docente, departamento_academico, tipo_contrato, docente_grupo

# Register your models here.
admin.site.register(docente)
admin.site.register(disponibilidad_docente)
admin.site.register(departamento_academico)
admin.site.register(tipo_contrato)
admin.site.register(docente_grupo)
