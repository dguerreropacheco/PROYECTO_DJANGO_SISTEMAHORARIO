from django.urls import path
from . import views

urlpatterns = [
    path('docente/', views.docente),
    path('csv/', views.upload_file),
    path('asignacionCargaLectiva/', views.asignacionCargaLectiva, name='asignacionCargaLectiva'),
    path('disponibilidadDocente/', views.disponibilidadDocente),
    path('gestionarDocente/', views.gestionarDocente, name="gestionarDocente"),
    path('agregarDocente/', views.agregarDocente, name="agregarDocente"),
    path('modificarDocente/<int:docente_id>/', views.modificar_docente, name='modificar_docente'),
    path('eliminarDocente/<int:docente_id>/', views.eliminar_docente, name='eliminar_docente'),
]