from django.contrib import admin
from .models import facultad, escuela, plan_estudio, tipo_curso, curso
# Register your models here.
admin.site.register(facultad)
admin.site.register(escuela)
admin.site.register(plan_estudio)
admin.site.register(curso)
admin.site.register(tipo_curso)