from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models.base import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.views.generic import DetailView, View
from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import ensure_csrf_cookie
from django.template import RequestContext
from django.urls import reverse
from django.core import serializers


from datetime import date
import re
import urlparse
import json

from herramientas import *
from models import *
from forms import *

# Create your views here.
def home(request):

    artistas = Perfil.public.all().order_by('visitas')[:4]
    eventos = Actividad.public.all().order_by('-fechaRealizacion')[:3]
    capsula = None
    try:
        capsula = Capsulas.objects.all().filter(fechaPublicacion__range=('2016-01-01',date.today())).order_by('-fechaPublicacion')[0]
    except IndexError:
        pass

    context = {
        'artistas' : artistas,
        'eventos' : eventos,
        'capsula' : capsula,
    }
    return render(request, 'index-v1.html', infoHome(request, context))

def perfil_list(request):
    limit = 10
    aumento = 10
    total = False

    if request.GET:
        limit=request.GET['limit']
        limit = int(limit)

    perfil = Perfil.public.all()[:limit]

    if len(perfil) != limit:
        total = True

    context = {
        'perfiles': perfil,
        'limit' : limit + aumento,
        'total' : total,
        'autorizar' : False
    }
    return render(request, 'artistas.html', infoHome(request,context))

def actividad_list(request):
    limit = 10
    aumento = 10
    total = False

    if request.GET:
        limit=request.GET['limit']
        limit = int(limit)

    actividad = Actividad.public.all()[:limit]

    if len(actividad) != limit:
        total = True

    context = {
        'actividad': actividad,
        'limit' : limit + aumento,
        'total' : total,
        'autorizar' : False
    }
    return render(request, 'actividades.html', infoHome(request,context) )

def categoria_list(request):
    categoria = Categoria.objects.all()

    context = {
        'categorias' : categoria,
    }

    return render(request, 'lista_categorias.html', infoHome(request,context))

def categoria(request, id=''):
    opcion = 1

    if request.method == 'POST':
        opcion = request.POST['op']


    categoria = Categoria.objects.get(id=int(id))

    actividad = Actividad.public.filter(categoria=categoria)
    perfil = Perfil.public.filter(categoria=categoria)

    context = {
        'categoria' : categoria,
        'actividad' : actividad,
        'perfil' : perfil,
        'opcion' : opcion,
    }

    return render(request, 'categoria.html', infoHome(request,context))

@login_required
def actividad_user(request, username=''):
    user = get_object_or_404(User, username=username)
    if request.user == user:
        actividad = Actividad.public.filter(perfil=request.user.perfil)
    else:
        return HttpResponseRedirect(reverse('error'))

    context = {'actividad': actividad, 'perfil': user}
    return render(request, 'mis_actividades.html', context)

@login_required
def actividad_to_authorize(request):
    if request.user.perfil.rol.is_admin() != True:
        return HttpResponseRedirect(reverse('error'))

    limit = 10
    aumento = 10
    total = False

    if request.GET:
        limit=request.GET['limit']
        limit = int(limit)

    actividades = Actividad.objects.filter(autorizado=0)[:limit]

    if len(actividades) != limit:
        total = True

    context = {
        'actividades': actividades,
        'limit' : limit + aumento,
        'total' : total,
    }
    return render(request, 'autorizar_actividad.html', infoHome(request,context))

@login_required
def artista_to_authorize(request):
    if request.user.perfil.rol.is_admin() != True:
        return HttpResponseRedirect(reverse('error'))

    limit = 10
    aumento = 10
    total = False

    if request.GET:
        limit=request.GET['limit']
        limit = int(limit)

    perfiles = Perfil.objects.filter(autorizado=0,rol__nombreRol='Artista')[:limit]

    if len(perfiles) != limit:
        total = True

    context = {
        'perfiles': perfiles,
        'limit' : limit + aumento,
        'total' : total,
    }
    return render(request, 'autorizar_artista.html', infoHome(request,context))

class EventosDetailView(DetailView):
    model = Perfil

    def get_context_data(self, **kwargs):
        context = super(EventosDetailView, self).get_context_data(**kwargs)
        actividades = Actividad.objects.filter(perfil=context['object']).order_by('fechaRealizacion')
        context = {'actividad': actividades}
        return context

#ajax request
def perfil_create_p1(request):
    if request.method == 'POST':
        response_data = {}
        username = request.POST['usuario']
        password = request.POST['contrasenia']
        password_confirm = request.POST['r_contrasenia']
        nombre = request.POST['nombre']
        email = request.POST['email']
        telefono = request.POST['telefono']
        nacimiento = request.POST['nacimiento']
        genero = request.POST['sexo']
        if genero == 'True':
            genero = True
        else:
            genero = False
        try:
            User.objects.get(username=username)
            response_data['existe'] = 'true'
            return JsonResponse(response_data)

        except ObjectDoesNotExist :

            estado, mensaje = validar_password(username, password,password_confirm)
            if estado:
                perfil = Perfil(nombreArtista = nombre, nombreReal = nombre, email=email, telefono=telefono,fechaNacimiento= nacimiento,sexo=genero)
                perfil.rol = get_object_or_404(Rol, nombreRol='Artista')
                nuevo_usuario = User.objects.create_user(username=username, email='xela@casacult.com', password=password)
                perfil.user = nuevo_usuario
                perfil.save()
                return JsonResponse(response_data)
            else:
                response_data['existe'] = 'true'
                response_data['error'] = 'true'
                response_data['mensaje'] = mensaje
                return JsonResponse(response_data)

    else:
        return HttpResponseBadRequest()

def perfil(request, username=''):

    user = get_object_or_404(User, username=username)
    if user.perfil.autorizado == False:
        if request.user.is_authenticated == False:
            return  HttpResponseRedirect(reverse('error'))
        if request.user.perfil.rol.is_admin() != True:
            return  HttpResponseRedirect(reverse('error'))

    perfil = user.perfil
    is_owner = False

    if request.user == user:
        is_owner = True

    conteo = request.session.get('conteo' + username,False)
    if conteo == False and is_owner == False and perfil.autorizado == True:
        visita = VisitasPerfil(perfil = perfil)
        visita.save()
        perfil.visitas = perfil.visitas + 1
        perfil.save()
        request.session['conteo' + username] = True

    context = {
        'perfil': perfil,
        'es_propietario': is_owner,
        'autorizado' : perfil.autorizado,
    }
    return render(request, 'detalle_artista.html', infoHome(request,context))

@login_required
def perfil_edit(request, username=''):
    user = get_object_or_404(User, username=username)

    if request.user != user or request.user.perfil.autorizado == False:
        return HttpResponseRedirect(reverse('error'))

    if request.method == 'POST':
        response_data = {}
        nombreArtista = request.POST['nombreArtista']
        nombreReal = request.POST['nombre']
        genero = request.POST['genero']
        if genero == 'True':
            genero = True
        else:
            genero = False
        nacimiento = request.POST['nacimiento']
        telefono = request.POST['telefono']
        email = request.POST['email']
        descripcion = request.POST['descripcion']
        categoria = request.POST['categoria']

        perfil = user.perfil
        perfil.nombreArtista = nombreArtista
        perfil.nombreReal = nombreReal
        perfil.sexo = genero
        perfil.fechaNacimiento = nacimiento
        perfil.telefono = telefono
        perfil.email = email
        perfil.descripcion = descripcion

        img = request.FILES.get('imagen', None)
        if img != None:
            img.name = renombrar_archivo(img.name,newName='perfil')
            perfil.imagen = img
            perfil.save()
            reescalar_imagen(perfil.imagen.path,perfil.imagen.path,height=300,width=300)

        perfil.save()
        perfil.categoria =  Categoria.objects.filter(categoria=categoria)

        return HttpResponseRedirect(reverse('home:perfil',kwargs={'username': request.user.username,}))

    context = {'perfil' : user.perfil}
    return render(request, 'editar_perfil.html', infoHome(request, context))

@login_required
def actividad_create(request,username=''):
    user = get_object_or_404(User, username=username)

    if request.user != user or request.user.perfil.autorizado == False:
        return HttpResponseRedirect(reverse('error'))

    if request.method == 'POST':
        response_data = {}
        nombre = request.POST['nombre']
        lugar = request.POST['lugar']
        fecha = request.POST['fecha']
        hora = request.POST['hora']
        descripcion = request.POST['descripcion']
        categoria = request.POST['categoria']

        actividad = Actividad(nombre=nombre, lugar=lugar, fechaRealizacion=fecha, hora=hora, descripcion=descripcion)

        img = request.FILES.get('imagen')
        if img != None:
            img.name = renombrar_archivo(img.name,newName='actividad')
            actividad.imagen = img
            actividad.save()
            reescalar_imagen(actividad.imagen.path,actividad.imagen.path)



        actividad.save()
        actividad.categoria = Categoria.objects.filter(categoria=categoria)
        actividad.perfil.add(request.user.perfil)
        return HttpResponseRedirect(reverse('home:confirmar_actividad'))


    return render(request, 'crear_actividad.html', infoHome(request,{}))

@login_required
def anadir_colaborador(request, username='', id=''):
    actividad = get_object_or_404(Actividad, id=int(id))

    if request.method == 'POST':
        colaborador = request.POST['colaborador']

        user = Perfil.objects.filter(nombreArtista=colaborador)
        actividad.perfil.add(user)

    context = {
    'actividad' : actividad
    }

    return render(request, 'editar_actividad.html', context)

@login_required
def anadir_imagen(request, username='', id=''):
    user = get_object_or_404(User, username=username)
    actividad = get_object_or_404(Actividad, id=int(id))

    if actividad.perfil.get().user.username != username:
        return HttpResponseRedirect(reverse('error'))

    if request.method == 'POST':
        img = request.FILES.get('imagen')
        if img != None:
            img.name = renombrar_archivo(img.name,newName='actividad')
            imagen = Imagenes(imagen=img, actividad=actividad)
            #actividad.imagen.add = img
            imagen.save()
            reescalar_imagen(imagen.imagen.path,imagen.imagen.path)

    context = {
        'actividad' : actividad,
    }

    return render(request, 'editar_actividad.html', context)

@login_required
def capsula_create(request):
    if request.user.perfil.rol.is_admin() != True:
        return HttpResponseRedirect(reverse('error'))

    if request.method == 'POST':
        fecha = request.POST['publicacion']
        texto = request.POST['texto']
        capsula = Capsulas(fechaPublicacion=fecha,texto=texto,usuario=request.user)
        capsula.save()
        return mensaje(request, 'Capsula Creada Exitosamente', reverse('ver_capsulas'))


    context = {'create': True}
    return render(request, 'capsula_detalle.html', context)

@login_required
def editar_capsula(request, pk = ''):
    if request.user.perfil.rol.is_admin() != True:
        return HttpResponseRedirect(reverse('error'))

    capsula = get_object_or_404(Capsulas, id=int(pk))

    if request.method == 'POST':
        capsula.fechaPublicacion = request.POST['publicacion']
        capsula.texto = request.POST['texto']
        capsula.usuario = request.user
        capsula.save()
        return mensaje(request, 'Capsula Modificada Exitosamente',reverse('ver_capsulas'))

    context = {'capsula': capsula,
                'create': False}
    return render(request, 'capsula_detalle.html', infoHome(request,context))

@login_required
def capsula_list(request):
    if request.user.perfil.rol.is_admin() != True:
        return HttpResponseRedirect(reverse('error'))

    limit = 10
    aumento = 10
    total = False

    if request.GET:
        limit=request.GET['limit']
        limit = int(limit)

    capsulas = Capsulas.objects.all().order_by('-fechaPublicacion')[:limit]

    if len(capsulas) != limit:
        total = True

    context = {
        'capsulas' : capsulas,
        'limit' : limit + aumento,
        'total' : total
    }
    return render(request, 'capsulas.html', infoHome(request,context))

@login_required
def administracion(request):
    if request.user.perfil.rol.is_admin() != True:
        return HttpResponseRedirect(reverse('error'))

    return render(request, 'administracion.html', infoHome(request, {}))

#ajax request
def ingresar(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home:home'))

    if request.method == 'GET':
        response_data = {}
        return HttpResponseRedirect(reverse('home:home'))
        #return JsonResponse(response_data)

    if request.method == 'POST':
        response_data = {}

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.perfil.rol.is_admin():
                login(request, user)
                return JsonResponse(response_data)
            if user.perfil.autorizado == True:
                login(request, user)
                return JsonResponse(response_data)
            else:
                response_data['autorizado'] = False
                return JsonResponse(response_data)
        #else:
        #    error = True
    return HttpResponseBadRequest()
    #context = {'create': True}

def ingresar_pagina(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home:home'))
    return render(request, 'login.html', infoHome(request, {}))

@login_required
def cerrar_sesion(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect(reverse('home:home'))

def error(request):
    return render(request, '404.html', infoHome(request, {}))

def actividad_detail(request, username='', id=''):
    user = get_object_or_404(User, username=username)
    actividad = Actividad.objects.get(id=int(id))
    actividades = Actividad.public.all()[:5]
    categoria = Categoria.objects.all()
    comentario = Comentarios.objects.filter(actividad=actividad)

    if actividad.perfil.get().user.username != username:
        return HttpResponseRedirect(reverse('error'))

    if actividad.autorizado == False:
        if request.user.is_authenticated == False:
            return  HttpResponseRedirect(reverse('error'))
        if request.user.perfil.rol.is_admin() != True:
            return  HttpResponseRedirect(reverse('error'))

    perfil = user.perfil
    is_owner = False

    if actividad.perfil == perfil.id:
        print 'true'
        is_owner = True

    conteo = request.session.get('conteo' + id, False)
    if conteo == False and actividad.autorizado == True:
        visita = VisitasActividad(actividad = actividad)
        visita.save()
        actividad.visitas = actividad.visitas + 1
        actividad.save()
        request.session['conteo' + id] = True
        print False

    context = {
        'actividad': actividad,
        'actividades': actividades,
        'categoria': categoria,
        'comentario' : comentario,
        'es_propietario': is_owner,
        'autorizado' : actividad.autorizado,
    }
    return render(request, 'detalle_actividad.html', infoHome(request, context))

def mensaje(request, mensaje='', path=''):
    if mensaje == None:
        return HttpResponseRedirect(reverse('error'))

    context={
        'mensaje':mensaje,
        'path' : path,
    }
    return render(request, 'mensaje.html', infoHome(request, context))

@login_required
def actividad_authorize(request, id=''):
    if request.user.perfil.rol.is_admin() != True:
        return HttpResponseRedirect(reverse('error'))

    actividad = get_object_or_404(Actividad, id=int(id))
    if actividad.autorizado != 0:
        return HttpResponseRedirect(reverse('error'))
    actividad.autorizado = 1
    actividad.save()

    return mensaje(request, 'Evento autorizado', reverse('actividad_pendiente'))

@login_required
def actividad_reject(request, id=''):
    if request.user.perfil.rol.is_admin() != True:
        return HttpResponseRedirect(reverse('error'))

    actividad = get_object_or_404(Actividad, id=int(id))
    if actividad.autorizado != 0:
        return HttpResponseRedirect(reverse('error'))
    actividad.delete()

    return mensaje(request, 'Evento rechazado', reverse('actividad_pendiente'))

@login_required
def artista_authorize(request, id=''):
    if request.user.perfil.rol.is_admin() != True:
        return HttpResponseRedirect(reverse('error'))

    artista = get_object_or_404(Perfil, id=int(id))
    if artista.autorizado != 0 or artista.user.perfil.rol.is_admin == True:
        return HttpResponseRedirect(reverse('error'))
    artista.autorizado = 1
    artista.save()

    return  mensaje(request, 'Artista autorizado', reverse('artista_pendiente'))

@login_required
def artista_reject(request, id=''):
    if request.user.perfil.rol.is_admin() != True:
        return HttpResponseRedirect(reverse('error'))

    artista = get_object_or_404(Perfil, id=int(id))
    if artista.autorizado != 0:
        return HttpResponseRedirect(reverse('error'))
    user = artista.user
    artista.delete()
    user.delete()

    return  mensaje(request, 'Artista rechazado', reverse('artista_pendiente'))

@login_required
def actividad_delete(request):
    id = request.POST.get('id')
    print id
    actividad = Actividad.objects.get(pk=id)
    actividad.delete()

    response = {}

    return JsonResponse(response)

def search_artista(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']
    else:
        search_text = ''

    if search_text == '':
        search_text = ' '

    perfil = Perfil.public.filter(nombreArtista__startswith= search_text)

    context = {
        'perfil':perfil,
    }

    return render(request, 'buscar_artistas.html', context)

def search_actividad(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']
    else:
        search_text = ''

    if search_text == '':
        search_text = ' '

    actividad = Actividad.public.filter(nombre__startswith= search_text)

    context = {
        'actividad':actividad,
    }

    return render(request, 'buscar_actividades.html', context)

@login_required
def estadisticas(request):
    if request.user.perfil.rol.is_admin() != True:
        return HttpResponseRedirect(reverse('error'))

    grafico = None
    g = GenGraficos()

    if request.GET:
        tipoE=request.GET['type']
        tipoG=request.GET['g']
        grafico = g.generarGrafico(g.getTipoGrafica(tipoG),g.getTipoEstadistica(tipoE))

    context={
        'grafico':grafico,
    }
    return render(request, 'estadisticas.html', context)

def confirmar_registro(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('error'))
    else:
        return render(request, 'confirmar_registro.html', infoHome(request, {}))

def confirmar_actividad(request):
    return render(request, 'confirmar_actividad.html', infoHome(request, {}))

def comentarios(request, id=''):
    if request.method == 'POST':
        response_date = {}
        texto = request.POST['texto']

        comentario = Comentarios(contenido=texto, fechaComentario=date.today())
        comentario.actividad = Actividad.objects.get(id=int(id))

        comentario.save()

    return JsonResponse(response_date)

@login_required
def cambiar_contrasenia(request, username=''):
    user = get_object_or_404(User, username=username)

    if request.user != user or request.user.perfil.autorizado == False:
        return HttpResponseRedirect(reverse('error'))

    if request.method == 'POST':
        response_data = {}
        actual = request.POST['actual']
        user = authenticate(username=request.user.username, password=actual)
        if user == None:
            response_data['error'] = True
            response_data['mensaje'] = 'Error'
            return JsonResponse(response_data)
        nueva = request.POST['nueva']
        confirmacion = request.POST['confirmacion']
        valido, mensaje = validar_password('username',nueva,confirmacion)
        if valido == True:
            request.user.set_password(nueva)
            request.user.save()
            login(request, request.user)
            return JsonResponse(response_data)
        response_data['error'] = True
        response_data['mensaje'] = mensaje
        return JsonResponse(response_data)

    return render(request, 'cambiar_contrasenia.html', infoHome(request, {}))

def ayuda(request):
    return render(request, 'ayuda.html', infoHome(request, {}))

def informacion(request):
    return render(request, 'about.html', infoHome(request, {}))

@login_required
def categoria_admin(request):
    if request.user.perfil.rol.is_admin() != True:
        return HttpResponseRedirect(reverse('error'))

    limit = 10
    aumento = 10
    total = False

    if request.GET:
        limit=request.GET['limit']
        limit = int(limit)

    categorias = Categoria.objects.all()[:limit]

    if len(categorias) != limit:
        total = True

    context = {
        'categorias' : categorias,
        'limit' : limit + aumento,
        'total' : total
    }
    return render(request, 'admin_categorias.html', infoHome(request,context))

@login_required
def categoria_crear(request):
    if request.user.perfil.rol.is_admin() != True:
        return HttpResponseRedirect(reverse('error'))

    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        categoria = Categoria(categoria=nombre,descripcion=descripcion)
        img = request.FILES.get('imagen', None)
        if img != None:
            img.name = renombrar_archivo(img.name,newName='cat')
            categoria.imagen = img
            #reescalar_imagen(perfil.imagen.path,perfil.imagen.path,height=300,width=300)

        categoria.save()
        return mensaje(request, 'Categoria Creada Exitosamente', reverse('admin_categoria'))


    context = {'create': True}

    return render(request, 'crear_categoria.html', infoHome(request,context))

@login_required
def categoria_editar(request, id=''):
    if request.user.perfil.rol.is_admin() != True:
        return HttpResponseRedirect(reverse('error'))

    categoria = get_object_or_404(Categoria, id=int(id))

    if request.method == 'POST':
        categoria.nombre = request.POST['nombre']
        categoria.descripcion = request.POST['descripcion']
        img = request.FILES.get('imagen', None)
        if img != None:
            img.name = renombrar_archivo(img.name,newName='cat')
            categoria.imagen = img
            #reescalar_imagen(perfil.imagen.path,perfil.imagen.path,height=300,width=300)
        categoria.save()

        return mensaje(request, 'Categoria Modificada Exitosamente',reverse('admin_categoria'))

    context = {'categoria': categoria,
                'create': False}

    return render(request, 'crear_categoria.html', infoHome(request,context))

def buscar_artista(request):
    if request.method == 'POST':
        search_text = request.POST['buscar']

    limit = 10
    aumento = 10
    total = False

    perfil = Perfil.public.filter(nombreArtista__startswith= search_text)[:limit]
    perfil = Perfil.public.filter(nombreReal__startswith= search_text)[:limit]

    if request.GET:
        limit=request.GET['limit']
        limit = int(limit)


    if len(perfil) != limit:
        total = True

    context = {
        'perfiles': perfil,
        'limit' : limit + aumento,
        'total' : total,
        'autorizar' : False
    }

    return render(request, 'resultados_busqueda.html', context)

@login_required
def imagenes_home(request):
    if request.user.perfil.rol.is_admin() != True:
        return HttpResponseRedirect(reverse('error'))

    imagenes = get_object_or_404(ImagenesHome, id=1)

    if request.method == 'POST':
        logo = request.FILES.get('logo', None)
        homeU = request.FILES.get('homeU', None)
        homeD = request.FILES.get('homeD', None)
        homeT = request.FILES.get('homeT', None)

        if logo != None:
            logo.name = renombrar_archivo(logo.name,newName='logo')
            imagenes.logo = logo
        if homeU != None:
            homeU.name = renombrar_archivo(homeU.name,newName='homeU')
            imagenes.homeU = homeU
        if homeD != None:
            homeD.name = renombrar_archivo(homeD.name,newName='homeD')
            imagenes.homeD = homeD
        if homeT != None:
            homeT.name = renombrar_archivo(homeT.name,newName='homeT')
            imagenes.homeT = homeT

        imagenes.save()

        return mensaje(request, 'Imagenes Modificadas Exitosamente',reverse('editar_imagenes'))

    context = {'imagenes': imagenes,}

    return render(request, 'imagenes_home.html', context)
