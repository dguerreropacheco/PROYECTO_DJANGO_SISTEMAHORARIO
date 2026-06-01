from django.contrib import admin
from django.urls import path, include
from modulo_usuario import views  # Importamos las vistas

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.login_view, name='login'),
    path('usuario/', include('modulo_usuario.urls')),
    path('horario/', include('modulo_horario.urls')),
    path('docente/', include('modulo_docente.urls')),
    path('curso/', include('modulo_curso.urls')),
    path('ambiente/', include('modulo_ambiente.urls')),
]