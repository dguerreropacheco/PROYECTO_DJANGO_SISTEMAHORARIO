from collections import defaultdict
from pyexpat import model
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.views.decorators.http import require_POST
from datetime import date, datetime, timedelta
from modulo_curso.models import escuela , plan_estudio, curso
from modulo_horario.models import escuela_ambiente, grupo_horario,dia_semana,horario,escuela_ambiente,horario, ciclo_academico
from modulo_docente.models import disponibilidad_docente, docente, docente_grupo
from modulo_ambiente.models import ambiente, edificio, tipo_ambiente
from pulp import LpMinimize, LpProblem, LpVariable, lpSum
from ortools.sat.python import cp_model
from datetime import datetime, time

# Create your views here.

def inicio(request):
    return render(request,'index.html')

def menuHorario(request):
    return render(request,'menuHorario.html')

def menuCurso(request):
    return render(request,'menuCurso.html')

def menuDocente(request):
    return render(request,'menuDocente.html')

def menuAmbiente(request):
    return render(request,'menuAmbiente.html')

def horariogestionar(request):
    return HttpResponse("Gestionar horario")


def login(request):
    return render(request,'Login.html')


def obtenerGruposHorariosDocentes(docente_seleccionado):
    enviar=[]
    docentes=[]
    
    gh = grupo_horario.objects.filter(fk_ciclo=1)
             
    for grupo_obj in gh:
                
                g_id = grupo_obj.id
                nombre = grupo_obj.fk_curso
                g_nombre = grupo_obj.grupo
                ghdocente= docente_grupo.objects.filter(FKgrupo=g_id)

                docentes = [ghdobj.FKdocente for ghdobj in ghdocente]

                if docente_seleccionado in docentes:
                    enviar.append((nombre, g_nombre, docente_seleccionado,g_id))
    
    return enviar


def horarioDocente(request):
    ids_docente = docente_grupo.objects.values_list('FKdocente_id', flat=True).distinct()
    docentes = docente.objects.filter(id__in=ids_docente).order_by('doc_nombres')
    horario_final = None
    docente_id = None
    ghs=[]
    horario_final = []
    horas = [(time(i).strftime('%H:%M'), i) for i in range(7, 22)]

    if request.method == 'POST':
        docente_id = request.POST.get('docente_sel')
        try:
            docente_seleccionado = docente.objects.get(id=docente_id)
            
            ghs= obtenerGruposHorariosDocentes(docente_seleccionado)
            
            for gh in ghs:
                horarios = horario.objects.filter(fk_grupo_horario_id=gh[3])
                for disp in horarios:
                    dia_nombre = disp.día_id
                    dia_nombre_f=dia_semana.objects.get(id=dia_nombre)
                    
                    hor_id = disp.id

                    hora_inicio = disp.hora_de_inicio
                    hora_de_inicio_obj = datetime.strptime(hora_inicio, '%H:%M:%S')
                    hora_iniciof = hora_de_inicio_obj.strftime('%H:%M')

                    hora_fin = disp.hora_final
                    hora_fin_obj = datetime.strptime(hora_fin, '%H:%M:%S')
                    hora_finf = hora_fin_obj.strftime('%H:%M')

                    amb= disp.ambiente
                    curgh=grupo_horario.objects.get(id=gh[3])

                    horario_final.append((dia_nombre_f.dia_nombre, hora_iniciof, hora_finf,amb.nombre_ambiente,curgh.fk_curso, curgh.grupo, curgh.fk_curso.ciclo_curso,hor_id))

        except docente.DoesNotExist:
            pass

        dias_semana = list(dia_semana.objects.values_list('dia_nombre', flat=True))
        return render(request, 'horarioDocentes.html', 
            {
             'docentes': docentes,
             'horario': horario_final,
             'dias_semana': dias_semana,
             #!agregado
             'horas': horas,  # Pasa la lista de horas a la plantilla
             'docente_id': int(docente_id),
         })
    
    else:
        return render(request, 'horarioDocentes.html', {
            'docentes': docentes,
        })




def horarioXCiclo(request):
    ciclos_distintos = horario.objects.select_related(
        'fk_grupo_horario__fk_curso'
    ).values(
        'fk_grupo_horario__fk_curso__ciclo_curso'
    ).distinct()
    listaCiclos = list(ciclos_distintos.values_list('fk_grupo_horario__fk_curso__ciclo_curso', flat=True))
    listaCiclos = [str(ciclo) for ciclo in listaCiclos]

    horas = [time(i).strftime('%H:%M') for i in range(7, 22)]  # Lista de horas de 07:00 a 22:00
    dias_semana = list(dia_semana.objects.values_list('dia_nombre', flat=True))

    ciclo_curso = None
    grupo_ciclo = None
    listaGrupos = []
    horario_final = []
    if request.method == 'POST':
        ciclo_curso = request.POST.get('ciclo_sel')
        grupo_ciclo = request.POST.get('grupo_sel')

        if ciclo_curso:
            listaGrupos = grupo_horario.objects.filter(fk_curso__ciclo_curso=ciclo_curso).values_list('grupo', flat=True).distinct()
            listaGrupos = [str(grupo) for grupo in listaGrupos]
        if ciclo_curso and grupo_ciclo:
            horarios = horario.objects.filter(
                fk_grupo_horario__fk_curso__ciclo_curso=ciclo_curso,
                fk_grupo_horario__grupo=grupo_ciclo
            ).select_related('fk_grupo_horario__fk_curso')

            horario_final = []
            for disp in horarios:
                dia_nombre = disp.día_id
                dia_nombre_f = dia_semana.objects.get(id=dia_nombre)

                hora_inicio = disp.hora_de_inicio
                hora_de_inicio_obj = datetime.strptime(hora_inicio, '%H:%M:%S')
                hora_iniciof = hora_de_inicio_obj.strftime('%H:%M')

                hora_fin = disp.hora_final
                hora_fin_obj = datetime.strptime(hora_fin, '%H:%M:%S')
                hora_finf = hora_fin_obj.strftime('%H:%M')

                amb = disp.ambiente
                curgh = grupo_horario.objects.get(id=disp.fk_grupo_horario_id)

                horario_final.append((dia_nombre_f.dia_nombre, hora_iniciof, hora_finf,
                                      amb.nombre_ambiente, curgh.fk_curso, curgh.grupo, curgh.fk_curso.ciclo_curso))
        else:
            horario_final = []

    return render(request, 'horarioPorCiclo.html', {
        'ciclos': listaCiclos,
        'grupos': listaGrupos,
        'horario': horario_final,
        'dias_semana': dias_semana,
        'horas': horas,
        'ciclo_curso': ciclo_curso,
        'grupo_ciclo': grupo_ciclo,
    })

def filtrar_ambientes_por_edificio(request):
    if request.method == 'POST':
        edificio_id = request.POST.get('edificio_id')
        ambientes = ambiente.objects.filter(FKedificio_id=edificio_id)
        ambientes_data = [{'id': amb.id, 'nombre': amb.nombre_ambiente} for amb in ambientes]
        return JsonResponse({'ambientes': ambientes_data})



#Reporte Horarios por Ambiente:
def horarios_por_ambiente(request):
    horario_final = None
    ambiente_id = None
    edificio_id = None
    semestre_id = None
    horarios_selected = []
    horario_final = []
    lista_semestres = ciclo_academico.objects.all()
    lista_edificios = edificio.objects.all()
    ids_ambiente = horario.objects.values_list('ambiente_id', flat=True).distinct()

    #! agregado
    horas = [time(i).strftime('%H:%M')
             for i in range(7, 22)]  # Lista de horas de 07:00 a 22:00

    
    
        
    semestre_select = request.POST.get('semestre_id')
    edificio_select = request.POST.get('edificio_id')
    ambiente_select = request.POST.get('ambiente_id')
    lista_ambientes = ambiente.objects.filter(id__in=ids_ambiente)

    
    if request.method == 'POST':
        

        if edificio_select:
            edif = edificio.objects.get(id=edificio_select)
            print ('edificio_select: ', edificio_select)
            print ('edif: ', edif.nombre_edificio)
            
            if ambiente_select and semestre_select:
                try:
                
                    amb = ambiente.objects.get(id=ambiente_select)
                    grupo_h_semestre = grupo_horario.objects.filter(fk_ciclo_id=semestre_select)
                    horarios = horario.objects.filter(ambiente_id=ambiente_select, fk_grupo_horario__in=grupo_h_semestre)
                    print(amb.nombre_ambiente)
                    for hor in horarios:
                        print ('hor: ', hor.día_id)
                        dia_nombre = hor.día_id
                        dia_nombre_f=dia_semana.objects.get(id=dia_nombre)
                        
                        hora_inicio = hor.hora_de_inicio
                        hora_de_inicio_obj = datetime.strptime(hora_inicio, '%H:%M:%S')
                        hora_iniciof = hora_de_inicio_obj.strftime('%H:%M')

                        hora_fin = hor.hora_final
                        hora_fin_obj = datetime.strptime(hora_fin, '%H:%M:%S')
                        hora_finf = hora_fin_obj.strftime('%H:%M')

                        grupo_h = grupo_horario.objects.get(id=hor.fk_grupo_horario_id)
                        print ('grupo_h: ', grupo_h.grupo)
                        curso_h = curso.objects.get(id=grupo_h.fk_curso_id)
                        print ('curso_h: ', curso_h.nombre_curso)

                        horario_final.append((dia_nombre_f.dia_nombre, hora_iniciof, hora_finf,amb.nombre_ambiente,curso_h, grupo_h.grupo, curso_h.ciclo_curso))

                except ambiente.DoesNotExist:
                    pass

                dias_semana = list(dia_semana.objects.values_list('dia_nombre', flat=True))
                return render(request, 'horarioAmbientes.html', 
                    {
                    'edificios': lista_edificios,
                    'edificio_seleccionado': int(edificio_select),
                    'semestre_sekcionado': semestre_select,
                    'semestres': lista_semestres,
                    'ambientes': lista_ambientes,
                    'horario': horario_final,
                    'dias_semana': dias_semana,
                    #!agregado
                    'horas': horas,  # Pasa la lista de horas a la plantilla
                    'ambiente_seleccionado': int(ambiente_select),
                })
            else:
                return render(request, 'horarioAmbientes.html', {
                    'edificios': lista_edificios,
                    'semestres': lista_semestres,
                    'ambientes': lista_ambientes,
                })

    else:
        return render(request, 'horarioAmbientes.html', {
                'edificios': lista_edificios,
                'semestres': lista_semestres,
                'ambientes': lista_ambientes,
            })


def obtenerCicloConcatenado_Obj(ciclo_seleccionado):
    ciclo_seleccion = ciclo_academico.objects.get(
                cic_año=ciclo_seleccionado.split(' - ')[0],
                cic_semestre=ciclo_seleccionado.split(' - ')[1])
    return ciclo_seleccion

def listadoGrupoHorario():
    grupos_horario = grupo_horario.objects.all()

    gruposhorarioarray=[]

    for grupo_obj in grupos_horario:
                g =  grupo_obj.grupo
                curso= grupo_obj.fk_curso
                cap= grupo_obj.capacidad
                ciclo= grupo_obj.fk_ciclo
                
                id= grupo_obj.id 
                gruposhorarioarray.append((ciclo,g,curso,cap, id))

    return gruposhorarioarray


def gestionarGrupoHorario(request):
    
    gruposhorarioarray=listadoGrupoHorario()

    if request.method == 'POST':
        
        
        return render(request, 'gestionarGrupoHorario.html', {
            'grupos_horario': gruposhorarioarray,
        })    
    else:
        
        return render(request, 'gestionarGrupoHorario.html', {
            'grupos_horario': gruposhorarioarray,
        })        
    
def obtenercurso():
    cursos = curso.objects.all()
    cursoarray = []
    for c in cursos:
        cursoarray.append(c.nombre_curso)
    return cursoarray

def obtenerciclo():
    ciclos = ciclo_academico.objects.all()
    cicloarray = []
    for ci in ciclos:
        cicloarray.append((f"{ci.cic_año} - {ci.cic_semestre}"))
    return cicloarray

def obtenerDocente():
    docentes = docente.objects.all()
    docentearray = []
    for d in docentes:
        docentearray.append(d.doc_nombres)
    return docentearray

def agregarGrupoHorario(request):
    cursos = obtenercurso()
    ciclos = obtenerciclo()

    if request.method == 'POST':
        grupo = request.POST.get('grupo')
        capacidad = request.POST.get('capacidad')
        ciclo = request.POST.get('ciclo')
        n_curso = request.POST.get('curso')
        
        ciclo_año, ciclo_semestre = ciclo.split(' - ')
        fkcic = ciclo_academico.objects.get(cic_año=ciclo_año, cic_semestre=ciclo_semestre)
        fkcur = curso.objects.get(nombre_curso=n_curso)

        nuevo_grupo_horario = grupo_horario(
            grupo=grupo,
            capacidad=capacidad,
            fk_ciclo=fkcic,
            fk_curso=fkcur,
        )
        
        # Guardar el nuevo grupo horario en la base de datos
        nuevo_grupo_horario.save()

        return redirect('gestionarGrupoHorario') 
    
    else:
        return render(request, 'agregarGrupoHorario.html', {'cursos': cursos, 'ciclos': ciclos})


def modificarGrupoHorario(request, grupo_id):
    grupo_horario_obj = get_object_or_404(grupo_horario, id=grupo_id)
    cursos = obtenercurso()
    ciclos = obtenerciclo()

    if request.method == 'POST':
        grupo = request.POST.get('grupo')
        capacidad = request.POST.get('capacidad')
        ciclo = request.POST.get('ciclo')
        n_curso = request.POST.get('curso')
        
        # Separar el año y el semestre del ciclo seleccionado
        ciclo_año, ciclo_semestre = ciclo.split(' - ')
        fkcic = ciclo_academico.objects.get(cic_año=ciclo_año, cic_semestre=ciclo_semestre)
        fkcur = curso.objects.get(nombre_curso=n_curso)

        # Actualizar el grupo horario existente
        grupo_horario_obj.grupo = grupo
        grupo_horario_obj.capacidad = capacidad
        grupo_horario_obj.fk_ciclo = fkcic
        grupo_horario_obj.fk_curso = fkcur
        
        # Guardar los cambios en la base de datos
        grupo_horario_obj.save()

        return redirect('gestionarGrupoHorario') 
    
    else:
        return render(request, 'modificarGrupoHorario.html', {
            'grupo_horario': grupo_horario_obj,
            'cursos': cursos,
            'ciclos': ciclos
        })
    

def eliminarGrupoHorario(request, grupo_id):
    grupo = grupo_horario.objects.get(id=grupo_id)
    #grupo = get_object_or_404(grupo_horario, id=grupo_id)
    
    if request.method == 'POST':
        respuesta = request.POST.get('respuesta')
        if respuesta == '1':
            grupo.delete()
        return redirect('gestionarGrupoHorario')
    
    return render(request, 'eliminarGrupoHorario.html', {'grupo': grupo})


def eliminarHorario(request, horario_id):
    horarios = horario.objects.get(id=horario_id)
    gru  = horarios.fk_grupo_horario
    nom = gru.fk_curso.nombre_curso
    
    if request.method == 'POST':
        respuesta = request.POST.get('respuesta')
        if respuesta == '1':
            horarios.delete()
        return redirect('horarioDocente')
    
    return render(request, 'eliminarHorario.html', {'horario': horarios, 'nombre_curso': nom})


# Funciones útiles

def obtenerCicloConcatenado_Obj(ciclo_seleccionado):
    ciclo_seleccion = ciclo_academico.objects.get(
                cic_año=ciclo_seleccionado.split(' - ')[0],
                cic_semestre=ciclo_seleccionado.split(' - ')[1])
    return ciclo_seleccion

def obtenerGruposHorariosDocentePorEscuelaCiclo(escuela_seleccion, ciclo_seleccion):
    
    enviar=[]
    docentes=[]
    
    planes = plan_estudio.objects.filter(fk_escuela=escuela_seleccion)

    for plan_estudio_obj in planes:
        cursos_filtrados = curso.objects.filter(
            FKplan_estudio_id=plan_estudio_obj)

        for curso_obj in cursos_filtrados:
            gh = grupo_horario.objects.filter(
                fk_ciclo=ciclo_seleccion.id, fk_curso=curso_obj)
            
            
            for grupo_obj in gh:
                
                g_id = grupo_obj.id
                nombre = grupo_obj.fk_curso
                g_nombre = grupo_obj.grupo

                ghdocente= docente_grupo.objects.filter(FKgrupo=g_id)

                if not ghdocente:
                    enviar.append((curso_obj.codigo_curso, curso_obj.ciclo_curso,nombre, g_nombre, "No tiene docente asignado",g_id))

                else:

                    docentes = [ghdobj.FKdocente for ghdobj in ghdocente]
                    docentes_str = ', '.join(str(doc) for doc in sorted(docentes, key=lambda x: x.id))

                    enviar.append((curso_obj.codigo_curso, curso_obj.ciclo_curso,nombre, g_nombre, docentes_str,g_id))
    
    return enviar




def obtenerHorariosDocentePorEscuelaCiclo(escuela_seleccion, ciclo_seleccion):
    
    enviar=[]
    docentes=[]
    plandoc=[]

    planes = plan_estudio.objects.filter(fk_escuela=escuela_seleccion)

    for plan_estudio_obj in planes:
        cursos_filtrados = curso.objects.filter(
            FKplan_estudio_id=plan_estudio_obj)

        for curso_obj in cursos_filtrados:
            gh = grupo_horario.objects.filter(
                fk_ciclo=ciclo_seleccion.id, fk_curso=curso_obj)
            
            
            for grupo_obj in gh:

                horarioo= horario.objects.filter(fk_grupo_horario_id=grupo_obj.id)

                for hor in horarioo:
                   hor_id= hor.id
                   g_id= hor.fk_grupo_horario_id
                   gcur= grupo_obj.fk_curso.nombre_curso
                   gcic= grupo_obj.fk_curso.ciclo_curso

                   ghs = docente_grupo.objects.filter(FKgrupo_id=g_id)

                   for gh in ghs:
                       
                       enviar.append((g_id, gcur,gcic,grupo_obj.grupo,hor.ambiente,gh.FKdocente.doc_nombres,hor.hora_de_inicio, hor.hora_final,hor.día,hor_id))

    
    return enviar



def obtenerDocentesPorEstado(estado):
    
    enviardoc=[]
    
    docentes = docente.objects.filter(doc_estado=estado)
    
    for docente_obj in docentes:
                nombre = docente_obj.doc_nombres
                id= docente_obj.id
                enviardoc.append((nombre,id))

    return enviardoc

def obtenerDocentesAsignados(id):

    enviar=[]

    ghdocente= docente_grupo.objects.filter(FKgrupo=id)

    if not ghdocente:
            enviar.append(("No hay asignados"))
    else:
        
        for ghdobj in ghdocente:
            
            objeto=docente.objects.get(doc_nombres=ghdobj.FKdocente)
            enviar.append((objeto.id,objeto.doc_nombres))

    return enviar

def prueba(request):
    ciclos = ciclo_academico.objects.all()
    escuelas = escuela.objects.all()
    
    ciclo_val = str(request.POST.get('ciclo_ac') or request.GET.get('ciclo_ac') or "")
    esc_val = str(request.POST.get('esc') or request.GET.get('esc') or "")
    
    context = {
        'ciclo_select': ciclos,
        'escuela_select': escuelas,
        'ciclo_seleccionado': ciclo_val,
        'escuela_seleccionada': esc_val,
        'amb': ambiente.objects.all(),
        'dias': dia_semana.objects.all(),
        'grupos': grupo_horario.objects.all(),
        'horarios': horario.objects.all()
    }

    if request.method == 'POST' and request.POST.get('action'):
        datos = {
            'hora_de_inicio': request.POST.get('hini'),
            'hora_final': request.POST.get('hfin'),
            'ambiente_id': request.POST.get('ambid'),
            'día_id': request.POST.get('diaid'),
            'fk_grupo_horario_id': request.POST.get('grid')
        }
        if request.POST.get('action') == 'nuevo':
            horario.objects.create(**datos)
        elif request.POST.get('horid'):
            h = horario.objects.get(id=request.POST.get('horid'))
            for k, v in datos.items(): setattr(h, k, v)
            h.save()

    if ciclo_val and esc_val:
        ciclo_obj = obtenerCicloConcatenado_Obj(ciclo_val)
        escuela_obj = escuela.objects.get(nombre_escuela=esc_val)
        context['cursos'] = obtenerHorariosDocentePorEscuelaCiclo(escuela_obj, ciclo_obj)
            
    return render(request, 'gestionarHorario.html', context)