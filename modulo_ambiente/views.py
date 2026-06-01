from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from modulo_horario.models import *
from modulo_curso.models import *
from modulo_ambiente.models import *
import json
from modulo_ambiente.forms import UploadCSVForm
from .models import ambiente
from .models import edificio
from .models import tipo_ambiente
from django.contrib import messages
import csv, io, openpyxl
from django.db.models import Count
# Create your views here.


# def ambiente(request):
#     return HttpResponse("ambientes disponibles")

def asignarAmbiente(request):
    return render(request,'asignarAmbiente.html')

#def csvAmbientes(request):
 #   return render(request,'csvAmbientes.html')

def obtenerSemestre(request):
    ciclos = ciclo_academico.objects.all()
    ciclos_list = list(ciclos.values('id', 'cic_año', 'cic_semestre'))
    return JsonResponse(ciclos_list, safe=False)

def obtenerEscuelas(request):
    escuelas = escuela.objects.all()
    escuelas_list = list(escuelas.values('id', 'nombre_escuela', 'director_escuela', 'fk_facultad_id'))
    return JsonResponse(escuelas_list, safe=False)

def obtenerCursosPorEscuela(request, escuela_id):
    try:
        cursos = curso.objects.filter(FKplan_estudio__fk_escuela_id=escuela_id)
        cursos_list = list(cursos.values('id', 'codigo_curso', 'nombre_curso', 'horas_totales', 'horas_practicas', 'horas_teoricas', 'ciclo_curso'))
        return JsonResponse(cursos_list, safe=False)
    except escuela.DoesNotExist:
        return JsonResponse({'error': 'La escuela no existe.'}, status=404)
def obtener_resumen_asignaciones(request):
    if request.method == 'GET':
        resumen = escuela_ambiente.objects.values('FK_ambiente__nombre_ambiente', 'FK_escuela__nombre_escuela').annotate(total=Count('FK_ambiente'))
        resumen_list = list(resumen)
        return JsonResponse(resumen_list, safe=False)
        

    else:
        return JsonResponse({'error': 'Método no permitido.'}, status=405)
def obtener_datos_reporte(request):
    if request.method == 'GET':
        datos = escuela_ambiente.objects.values('FK_escuela__nombre_escuela').annotate(total=Count('FK_ambiente')).order_by('FK_escuela__nombre_escuela')
        datos_list = list(datos)
        return JsonResponse(datos_list, safe=False)
        #return render(request, 'reporteAmbiente.html', JsonResponse(datos_list, safe=False))

    else:
        return JsonResponse({'error': 'Método no permitido.'}, status=405)
#def reporte_ambientes(request):
    #return render(request, 'reporteAmbiente.html')
def obtener_datos_reporte_ambiente_curso(request):
    if request.method == 'GET':
        # Obtener todos los cursos
        cursos = grupo_horario.objects.values('fk_curso__nombre_curso').distinct()

        resultado_final = []
        
        # Filtrar grupos con el mismo nombre de curso y obtener sus ambientes únicos
        for curso in cursos:
            nombre_curso = curso['fk_curso__nombre_curso']
            ambientes = horario.objects.filter(
                fk_grupo_horario__fk_curso__nombre_curso=nombre_curso
            ).values(
                'fk_grupo_horario__fk_curso__nombre_curso', 
                'ambiente__nombre_ambiente'
            ).distinct().annotate(total=Count('ambiente_id')).order_by('fk_grupo_horario__fk_curso__nombre_curso')
            
            resultado_final.extend(ambientes)

        return JsonResponse(resultado_final, safe=False)

        #return JsonResponse(resultado_final, safe=False)
    else:
        return JsonResponse({'error': 'Método no permitido.'}, status=405)

def reporte_ambiente_curso(request):
    return render(request, 'reporte_ambiente_curso.html')
#Obtiene todos los edificios y, para cada uno, obtiene los ambientes relacionados mediante una clave foránea.

def obtener_edificios_y_ambientes(request):
    edificios = edificio.objects.all()
    data = []

    for edif in edificios:
        ambientes = ambiente.objects.filter(FKedificio=edif).values('id','nombre_ambiente', 'capacidad_ambiente', 'estado_ambiente', 'piso')
        data.append({
            'id': edif.id,
            'nombre_edificio': edif.nombre_edificio,
            'ambientes': list(ambientes)
        })
    
    return JsonResponse(data, safe=False)
def obtener_edificio_id(request, nombre):
    #edificios = edificio.objects.filter(nombre_edificio=nombre)
    #edificio_list = list(edificios.values('id'))
    #return (edificio_list)
    #edificio_id = edificio_.id
    #return (edificio_id)
    
    try:
        return edificio.objects.get(nombre_edificio=nombre)
    except edificio.DoesNotExist:
        return None

    

def guardar_ambientes_seleccionados(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id_escuela = data.get('id_escuela')
        print(id_escuela)
        ambientes_seleccionados = data.get('ambientes_seleccionados')
        print(ambientes_seleccionados)
        try:
            for id_ambiente in ambientes_seleccionados:
                # Intenta guardar cada ambiente seleccionado en la base de datos
                horarioEscuela.objects.create(FKescuela_id=id_escuela, FKambiente_id=id_ambiente)

        except Exception as e:
            # Si hay un error al guardar algún ambiente, devuelve un mensaje de error
            return JsonResponse({'error': f'Error al guardar los ambientes: {str(e)}'}, status=500)
        else:
            # Si todos los ambientes se han guardado correctamente, devuelve un mensaje de éxito
            return JsonResponse({'mensaje': 'Todos los ambientes se han guardado exitosamente.'})
    else:
        return JsonResponse({'error': 'Método no permitido.'}, status=405)

def upload_file(request):
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            if 'Subir_archivo_excel' in request.FILES:
                excel_file = request.FILES['Subir_archivo_excel']
                workbook = openpyxl.load_workbook(excel_file)
                sheet = workbook.active
                try:
                    

                    # Skip the header
                    for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row, min_col=1, max_col=sheet.max_column):
                        if row is None or all(cell is None for cell in row):
                            continue  # Skip empty rows
                        #print(f"Procesando fila: {row}")
                        #print(f"Procesando ed: {row[2]}")
                        ambientes = edificio.objects.all()
                        nro, nombre_ambiente, nombre_edificio, aforo, piso, nombre_tipo_ambiente = [cell.value for cell in row]
                
# Iterar y mostrar cada instancia
                       
                        if row[1] and row[2]:
                            nombre = row[1]
                           
                            tipoa= row[5]
                            
                            
                            edificio_id = row[2]
                            edificios = edificio.objects.filter(nombre_edificio=nombre_edificio)

                            if not edificios:

                                if nombre_edificio is None:
                                    continue
                                else:
                                    print(f"No se encontró ningún edificio con el nombre '{nombre_edificio}'.")
                                    continue

                            tipos_ambiente = tipo_ambiente.objects.filter(tipo_de_ambiente=nombre_tipo_ambiente)
                            if not tipos_ambiente:
                                print(f"No se encontró ningún tipo de ambiente con el nombre '{nombre_tipo_ambiente}'.")
                                continue
                            
                            for edificio_obj in edificios:
                                for tipo_ambiente_obj in tipos_ambiente: 
                                    ambiente_obj = ambiente(
                                        nombre_ambiente=nombre_ambiente,
                                        capacidad_ambiente=aforo,
                                        estado_ambiente='D',  # Asumiendo que todos los ambientes están disponibles por defecto
                                        piso=piso,
                                        FKedificio=edificio_obj,
                                        FKtipo_ambiente=tipo_ambiente_obj
                                        )
                                    ambiente_obj.save()
                            
                            #messages.success(request, 'Los datos han sido cargados exitosamente.')
                           
                        else:
                            messages.warning(request, f'Fila incompleta o incorrecta: {row}')
                    messages.success(
                        request, 'Archivo Excel subido correctamente')
                except openpyxl.utils.exceptions.InvalidFileException:
                    messages.error(
                        request, 'El archivo subido no es un archivo Excel válido.')
                except Exception as e:
                    messages.error(request, f'Error: {str(e)}')

            return redirect(request.path)
    else:
        form = UploadCSVForm()
        enviar=obtener_ambientes_array()

    return render(request, './csvAmbientes.html', {'form': form, 'disponibilidad':enviar})


#Para obtener los ambientes asignados a cada escuela:
def obtener_edificios_y_ambientes_semestre_ciclo_academico(request):

    if request.method == 'POST':
        data = json.loads(request.body)
        semestre = data.get('semestre')
        escuela = data.get('escuela')

        ambientes_por_edificios = obtener_edificios_y_ambientes_seleccion(semestre, escuela)
        return JsonResponse(ambientes_por_edificios, safe=False)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)

#Llama a esta función:
def obtener_edificios_y_ambientes_seleccion(semestre_select, escuela_select):
    edificios = edificio.objects.all()

    
    
    ambientelist = []
    data = []

    for edif in edificios:
        
        ambientes = []
        

        if escuela_select and semestre_select:
            #escuela_se = escuela.objects.get(nombre_escuela="Ing. de sistemas")
            #semestre_se_split = str('2024 - 1').split(" - ")
            escuela_se = escuela.objects.get(id=escuela_select)
            semestre_se = ciclo_academico.objects.get(id=semestre_select)
            try:    
                escuela_ambiente_filtradas = escuela_ambiente.objects.filter(FK_ciclo_academico=semestre_se, FK_escuela=escuela_se)
            except escuela.DoesNotExist:
                grupo_ambientes = ambiente.objects.none()
            except ciclo_academico.DoesNotExist:
            #Maneja el caso en que el ciclo académico no existe
                grupo_ambientes = ambiente.objects.none()
            
            

            if escuela_ambiente_filtradas:
                ambiente_ids = escuela_ambiente_filtradas.values_list('FK_ambiente_id', flat=True)
                grupo_ambientes = ambiente.objects.filter(FKedificio=edif)
                
                for amb in grupo_ambientes:
                    if amb.id in ambiente_ids:
                        boton = str("ocupado")
                    else:
                        boton = str("no ocupado")
                    ambientes.append({
                            'id': amb.id,
                            'nombre_ambiente': amb.nombre_ambiente,
                            'capacidad_ambiente': amb.capacidad_ambiente,
                            'estado_ambiente': amb.estado_ambiente,
                            'piso': amb.piso,
                            'estado': boton
                        })
                      
                

            else:
                grupo_ambientes = ambiente.objects.filter(FKedificio=edif)
                for amb in grupo_ambientes:
                    boton = str("no ocupado")
                    ambientes.append({
                    'id': amb.id,
                    'nombre_ambiente': amb.nombre_ambiente,
                    'capacidad_ambiente': amb.capacidad_ambiente,
                    'estado_ambiente': amb.estado_ambiente,
                    'piso': amb.piso,
                    'estado': boton
                })

        else:
            grupo_ambientes = ambiente.objects.filter(FKedificio=edif)
            
            for amb in grupo_ambientes:
                boton = str("no ocupado")
                ambientes.append({
                    'id': amb.id,
                    'nombre_ambiente': amb.nombre_ambiente,
                    'capacidad_ambiente': amb.capacidad_ambiente,
                    'estado_ambiente': amb.estado_ambiente,
                    'piso': amb.piso,
                    'estado': boton
                })
        


        data.append({
            'id': edif.id,
            'nombre_edificio': edif.nombre_edificio,
            'ambientes': list(ambientes)
        })

    return data


#Proceso de asignar ambientes a escuelas.
#Falta configurar para enviar un mensaje para que se muestre en la pantalla y para bloquear/desbloquear el botón.
def guardar_ambientes_seleccionados(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print("Datos recibidos:", data)
        escuela_id = data.get('id_escuela')
        semestre_id = data.get('id_semestre')
        ambientes_seleccionados = data.get('ambientes_seleccionados')
        print("ID Escuela:", escuela_id)  # Mensaje de depuración
        print("ID Semestre:", semestre_id)  # Mensaje de depuración
        print("Ambientes seleccionados:", ambientes_seleccionados)
        

        try:
            escuela_se = get_object_or_404(escuela, id=escuela_id)
            semestre_se = get_object_or_404(ciclo_academico, id=semestre_id)
            escuela_ambiente_filtradas = escuela_ambiente.objects.filter(FK_ciclo_academico=semestre_se, FK_escuela=escuela_se)
            ambiente_ids = escuela_ambiente_filtradas.values_list('FK_ambiente_id', flat=True)
            print(str(ambiente_ids))

            for ambiente_data in ambientes_seleccionados:
                ambiente_id = ambiente_data.get('id')
                buttonClasses = str(ambiente_data.get('buttonClasses'))

                if int(ambiente_id) in ambiente_ids:
                    
                    if buttonClasses == 'success':
                        ambiente_se = get_object_or_404(ambiente, id=ambiente_id)
                        print('eliminando')
                        escuela_ambiente.objects.filter(FK_ciclo_academico=semestre_se, FK_escuela=escuela_se, FK_ambiente = ambiente_se).delete()
                else:
                    
                    if buttonClasses == 'danger':
                        print('creando')
                        ambiente_se = get_object_or_404(ambiente, id=ambiente_id)
                        escuela_ambiente.objects.create(
                            FK_escuela = escuela_se,
                            FK_ambiente = ambiente_se,
                            FK_ciclo_academico = semestre_se
                        )
                    
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
    

#Obtener ambientes en listado data
def obtener_ambientes_array():
    
    dispo= ambiente.objects.all();    
    enviar=[]

    for amobj in dispo:
        
        ambdispo=ambiente.objects.get(id=amobj.id)

        nombre= ambdispo.nombre_ambiente
        capa= ambdispo.capacidad_ambiente
        edificio= ambdispo.FKedificio
        piso = ambdispo.piso
        tipo = ambdispo.FKtipo_ambiente
        estado= ambdispo.estado_ambiente

        enviar.append((nombre,capa,edificio,piso,tipo,estado))

    return enviar




##gestionar

def obtener_ambientes_arrayconid():
    
    dispo= ambiente.objects.all();    
    enviar=[]

    for amobj in dispo:
        
        ambdispo=ambiente.objects.get(id=amobj.id)

        nombre= ambdispo.nombre_ambiente
        capa= ambdispo.capacidad_ambiente
        edificio= ambdispo.FKedificio
        piso = ambdispo.piso
        tipo = ambdispo.FKtipo_ambiente
        estado= ambdispo.estado_ambiente

        enviar.append((nombre,capa,edificio,piso,tipo,estado,ambdispo.id))

    return enviar

def obtener_tipo_ambiente():

    tpas= tipo_ambiente.objects.all();
    enviar=[]

    for tp in tpas:
        nombre= tp.tipo_de_ambiente

        enviar.append((nombre))

    return enviar


def obtener_edificios():

    tpas= edificio.objects.all();
    enviar=[]

    for tp in tpas:
        nombre= tp.nombre_edificio
        enviar.append((nombre))

    return enviar

def gestionarAmbiente(request):
    
    ambientesarrray=obtener_ambientes_arrayconid()

    if request.method == 'POST':
        
        
        return render(request, 'gestionarAmbiente.html', {
            'ambientes': ambientesarrray,
        })    
    else:
        
        return render(request, 'gestionarAmbiente.html', {
            'ambientes': ambientesarrray,
        })        
    

def agregarAmbiente(request):

    ambs=obtener_edificios()
    tps= obtener_tipo_ambiente()

    if request.method == 'POST':

        nombre = request.POST.get('nombre')
        capacidad = request.POST.get('capacidad')
        edificiom = request.POST.get('edificio')
        piso = request.POST.get('piso')
        tipoambiente = request.POST.get('tipoambiente')
        estado = request.POST.get('estado')  # 'D' o 'I' dependiendo del checkbox

        fktp= tipo_ambiente.objects.get(tipo_de_ambiente=tipoambiente)
        fked= edificio.objects.get(nombre_edificio=edificiom)


        nuevo_ambiente = ambiente(
            FKedificio_id=fked.id,
            FKtipo_ambiente_id=fktp.id,
            nombre_ambiente= nombre,
            capacidad_ambiente=capacidad,
            piso=piso,
            estado_ambiente=estado  # Asegúrate de que estado sea 'D' o 'I' según tu lógica
        )
        
        # Guardar el nuevo docente en la base de datos
        nuevo_ambiente.save()


        return redirect('gestionarAmbiente') 
    
    else:
        return render(request, 'agregarAmbiente.html', {'ambs':ambs,'tpas':tps})


def modificar_ambiente(request, ambiente_id):
    df = ambiente.objects.get(id=ambiente_id)
    
    datosenviar=[]
    datosenviar.append((df.nombre_ambiente, df.capacidad_ambiente, df.piso, df.FKedificio, df.FKtipo_ambiente, df.estado_ambiente))

    ambs=obtener_edificios()
    tps= obtener_tipo_ambiente()

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        capacidad = request.POST.get('capacidad')
        edificiom = request.POST.get('edificio')
        piso = request.POST.get('piso')
        tipoambiente = request.POST.get('tipoambiente')
        estado = request.POST.get('estado')  # 'D' o 'I' dependiendo del checkbox

        fktp= tipo_ambiente.objects.get(tipo_de_ambiente=tipoambiente)
        fked= edificio.objects.get(nombre_edificio=edificiom)

        # Actualizar los datos del docente
        df.nombre_ambiente = nombre
        df.capacidad_ambiente = capacidad
        df.piso = piso
        df.FKtipo_ambiente = fktp
        df.FKedificio = fked
        df.estado_ambiente = estado 

        df.save()  # Guardar los cambios en la base de datos

        return redirect('gestionarAmbiente') 

    return render(request, 'modificarAmbiente.html', {'docente': datosenviar,'ambs':ambs,'tpas':tps})



def eliminar_ambiente(request, ambiente_id):
    df = ambiente.objects.get(id=ambiente_id)
    
    datosenviar=[]
    tabladg=[]

    datosenviar.append((df.nombre_ambiente))
    label1=""

    dg=horario.objects.filter(ambiente_id=ambiente_id)

    if dg.count()>0:
        label1= "El docente tiene grupos horarios asignados"
    

    for dgs in dg:
        grupo=dgs.id

        gh=horario.objects.get(id=grupo)

        tabladg.append((gh))

    if request.method == 'POST':
        respuesta = request.POST.get('respuesta')
        if respuesta=='1':
            df.delete()  

        return redirect('gestionarAmbiente') 
    
    return render(request, 'eliminarAmbiente.html', {'docente': datosenviar, 'dg':tabladg,'msj2': label1})
