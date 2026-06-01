from django.urls import path
from . import views

urlpatterns = [
    path('ambiente/', views.ambiente),
    path('asignarAmbiente/', views.asignarAmbiente),
    path('obtener-semestre/', views.obtenerSemestre, name='obtenerSemestre'),
    path('obtener-escuelas/',views.obtenerEscuelas, name='obtenerEscuelas'),
    path('obtener-cursos/<int:escuela_id>/', views.obtenerCursosPorEscuela, name='obtenerCursosPorEscuela'),
    path('obtener-edificios-ambientes/', views.obtener_edificios_y_ambientes, name='obtener_edificios_ambientes'),
    path('obtener-edificios-ambientes-selected/', views.obtener_edificios_y_ambientes_semestre_ciclo_academico, name='obtener_edificios_y_ambientes_selected'),
    path('guardar-ambientes-seleccionados/', views.guardar_ambientes_seleccionados, name='guardar_ambientes_seleccionados'),
    path('csvAmbientes/', views.upload_file),
    path('gestionarAmbiente', views.gestionarAmbiente, name='gestionarAmbiente'),
    path('agregarAmbiente', views.agregarAmbiente, name='agregarAmbiente'),
    path('modificarAmbiente/<int:ambiente_id>/', views.modificar_ambiente, name='modificarAmbiente'),
    path('eliminarAmbiente/<int:ambiente_id>/', views.eliminar_ambiente, name='eliminarAmbiente'),
    path('resumen-asignaciones/', views.obtener_resumen_asignaciones, name='obtener_resumen_asignaciones'),
    path('datos-reporte/', views.obtener_datos_reporte, name='obtener_datos_reporte'),
    path('datos-reporte-ambiente-curso/', views.obtener_datos_reporte_ambiente_curso, name='obtener_datos_reporte_ambiente_curso'),
    path('reporte-ambiente-curso/', views.reporte_ambiente_curso, name='reporte_ambiente_curso')
]