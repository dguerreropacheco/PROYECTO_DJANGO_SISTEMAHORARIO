from django.contrib import admin
from .models import edificio, tipo_ambiente, ambiente
# Register your models here.
admin.site.register(edificio)
admin.site.register(tipo_ambiente)
admin.site.register(ambiente)

admin.site.site_header="Administración del Sistema de Gestión de Horarios Docentes"
admin.site.site_title="Administración del Sistema Gestión de Horarios Docentes"
admin.site.index_title=""


