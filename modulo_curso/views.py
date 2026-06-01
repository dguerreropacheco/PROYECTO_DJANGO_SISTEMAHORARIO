from django.shortcuts import redirect, render
from django.http import HttpResponse
from modulo_curso.models import escuela , plan_estudio, curso, tipo_curso
from modulo_horario.models import grupo_horario, ciclo_academico

# Create your views here.
def Obtenercurso(plan):
    plan_es = plan_estudio.objects.filter(plan_nombre=plan)
    cursos = curso.objects.filter(FKplan_estudio__in = plan_es)
    return cursos


def obtenerGruposHorarios(id):
    grupos = grupo_horario.objects.filter(fk_curso_id=id)
    
    listado=[]
    for gh in grupos:
        listado.append(gh.grupo)

    return listado

def grupoHorario(request):
    escuelas = escuela.objects.all()
    escuela_select = request.POST.get('escuela')
    plan_select = request.POST.get('plan_estudio')
    curso_list = []
    listado=[]

    if escuela_select:
        escuela_se = escuela.objects.get(nombre_escuela=escuela_select)
        plan = plan_estudio.objects.filter(fk_escuela_id=escuela_se.id)

        if plan_select:
            plan_se = plan_estudio.objects.get(plan_nombre=plan_select)
            print(plan_se)
            cursos_plan = Obtenercurso(plan_se)

            for cur in cursos_plan:

                listado=obtenerGruposHorarios(cur.id)
                listado_sin_corchetes = ', '.join(listado)
                curso_list.append({
                    'id': cur.id,
                    'codigo_curso': cur.codigo_curso,
                    'ciclo_curso': cur.ciclo_curso,
                    'nombre_curso': cur.nombre_curso,
                    'grupos': listado_sin_corchetes
                })

            if request.method == 'POST':
                for cur in curso_list:
                    if request.POST.get('seleccionado_' + str(cur['id'])):
                        cantidad = int(request.POST.get('cantidad_' + str(cur['id'])))
                        for i in range(cantidad):
                            ciclo = ciclo_academico.objects.last()
                            curso_id = curso.objects.get(id=cur['id'])
                            ultimo_grupo = grupo_horario.objects.filter(fk_curso=curso_id).order_by('-grupo').first()
                            if ultimo_grupo:
                                nuevo_nombre = chr(ord(ultimo_grupo.grupo) + 1)
                            else:
                                nuevo_nombre = 'A'
                            grupo_horario.objects.create(grupo=nuevo_nombre, fk_curso=curso_id,fk_ciclo=ciclo)

            data = {
                'escuela' : escuelas,
                'escuela_select' : escuela_select,
                'plan_estudio' : plan,
                'plan_select' : plan_se.plan_nombre,
                'cursos' : curso_list
            }
            return render(request, 'grupoHorario.html', data)
        else:
            data = {
                'escuela' : escuelas,
                'escuela_select' : escuela_select,
                'plan_estudio' : plan,
            }
            return render(request, 'grupoHorario.html', data)
    else:
        data = {
            'escuela' : escuelas,
        }
        return render(request, 'grupoHorario.html', data)
    


##gestionar

def obtenerCursos():
    grupos = curso.objects.all()
    
    listado=[]
    for gh in grupos:
        listado.append((gh.codigo_curso,gh.nombre_curso, gh.ciclo_curso, gh.horas_practicas, gh.horas_teoricas, gh.FKplan_estudio.plan_nombre, gh.id))

    return listado



def obtenerplanes():
    pl = plan_estudio.objects.all()
    
    listado=[]
    for gh in pl:
        listado.append((gh.plan_nombre,gh.id))

    return listado


def obtenertipcursos():
    pl = tipo_curso.objects.all()
    
    listado=[]
    for gh in pl:
        listado.append((gh.tipo_curso, gh.id))

    return listado

def gestionarCurso(request):

    cursoArray=obtenerCursos()

    if request.method == 'POST':
        
        return render(request, 'gestionarCurso.html', {
            'docentes': cursoArray,
        })    
    else:
        
        return render(request, 'gestionarCurso.html', {
            'docentes': cursoArray,
        })        


def agregarCurso(request):

    ambs=obtenertipcursos()
    tps= obtenerplanes()

    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        nombre = request.POST.get('nombre')
        hpracticas = request.POST.get('hpracticas')
        hteoricas = request.POST.get('hteoricas')
        ciclo = request.POST.get('ciclo')
        tcur = request.POST.get('tcur')
        plan = request.POST.get('plan')
        hsuma = request.POST.get('hsuma')


        fktp= tipo_curso.objects.get(tipo_curso=tcur)
        fked= plan_estudio.objects.get(plan_nombre=plan)


        nuevo_curso = curso(FKtipocurso_id=fktp.id, nombre_curso=nombre, FKplan_estudio_id=fked.id, horas_practicas=hpracticas, horas_teoricas=hteoricas, horas_totales= hsuma, codigo_curso=codigo, ciclo_curso=ciclo, amb=0
        )
        
        # Guardar el nuevo docente en la base de datos
        nuevo_curso.save()


        return redirect('gestionarCurso') 
    
    else:
        return render(request, 'agregarCurso.html', {'ambs':ambs,'tpas':tps})


def modificar_curso(request,curso_id):


    df = curso.objects.get(id=curso_id)
    
    datosenviar=[]
    datosenviar.append((df.codigo_curso, df.nombre_curso, df.horas_practicas, df.horas_teoricas, df.FKplan_estudio, df.FKtipocurso, df.ciclo_curso))


    ambs=obtenertipcursos()
    tps= obtenerplanes()


    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        nombre = request.POST.get('nombre')
        hpracticas = request.POST.get('hpracticas')
        hteoricas = request.POST.get('hteoricas')
        hsuma = request.POST.get('hsuma')
        ciclo = request.POST.get('ciclo')
        tcur = request.POST.get('tcur')
        plan = request.POST.get('plan')


        fktp= tipo_curso.objects.get(tipo_curso=tcur)
        fked= plan_estudio.objects.get(plan_nombre=plan)

        # Actualizar los datos del docente
        df.FKtipocurso_id=fktp.id
        df.nombre_curso=nombre
        df.FKplan_estudio_id=fked.id
        df.horas_practicas=hpracticas
        df.horas_teoricas=hteoricas
        df.horas_totales= hsuma
        df.codigo_curso=codigo
        df.ciclo_curso=ciclo



        df.save()  # Guardar los cambios en la base de datos

        return redirect('gestionarCurso') 

    return render(request, 'modificarCurso.html', {'docente': datosenviar,'ambs':ambs,'tpas':tps})



def eliminar_curso(request,curso_id):

    df = curso.objects.get(id=curso_id)
    
    datosenviar=[]

    datosenviar.append((df.nombre_curso))

    if request.method == 'POST':
        respuesta = request.POST.get('respuesta')
        if respuesta=='1':
            df.delete()  

        return redirect('gestionarCurso') 
    
    return render(request, 'eliminarCurso.html', {'docente': datosenviar})
