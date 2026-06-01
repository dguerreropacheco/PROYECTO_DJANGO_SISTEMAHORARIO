from django.contrib import admin
from .models import horario, dia_semana, ciclo_academico, grupo_horario, escuela_ambiente

# Register your models here.
admin.site.register(horario)
admin.site.register(dia_semana)
admin.site.register(ciclo_academico)
admin.site.register(grupo_horario)
admin.site.register(escuela_ambiente)
