from django.urls import path
from . import views

urlpatterns = [
    path('grupoHorario/', views.grupoHorario, name='grupoHorario'),
    path('gestionarCurso', views.gestionarCurso, name='gestionarCurso'),
    path('agregarCurso/', views.agregarCurso, name="agregarCurso"),
    path('modificarCurso/<int:curso_id>/', views.modificar_curso, name='modificar_curso'),
    path('eliminarCurso/<int:curso_id>/', views.eliminar_curso, name='eliminar_curso'),
]