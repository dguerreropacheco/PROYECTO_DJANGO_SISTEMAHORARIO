from django.urls import path
from . import views
from modulo_ambiente import *
from modulo_usuario.views import *

urlpatterns = [
    path('inicio/', views.inicio),
    path('horario/', views.horariogestionar),
    path('inicio/menuHorario/', views.menuHorario,  name="menu_horario"),
    path('inicio/menuCurso/', views.menuCurso,  name="menu_curso"),
    path('inicio/menuDocente/', views.menuDocente,  name="menu_docente"),
    path('inicio/menuAmbiente/', views.menuAmbiente,  name="menu_ambiente"),
    path('horarioPorDocente/',views.horarioDocente, name="horarioDocente"),
    path('horarioPorCiclo/',views.horarioXCiclo,name="horarioPorCiclo"),
    path('horarioPorAmbiente/',views.horarios_por_ambiente),
    path('filtrar_ambientes_por_edificio/', views.filtrar_ambientes_por_edificio, name='filtrar_ambientes_por_edificio'),
    path('gestionarGrupoHorario/', views.gestionarGrupoHorario, name="gestionarGrupoHorario"),
    path('agregarGrupoHorario/', views.agregarGrupoHorario, name="agregarGrupoHorario"),
    path('modificarGrupoHorario/<int:grupo_id>/', views.modificarGrupoHorario, name='modificarGrupoHorario'),
    path('eliminarGrupoHorario/<int:grupo_id>/', views.eliminarGrupoHorario, name='eliminarGrupoHorario'),
    path('gestionarHorario/', views.prueba, name="gestionarHorario"),   
        
]