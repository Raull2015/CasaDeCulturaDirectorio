from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models.base import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.views.generic import DetailView, View
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.urls import reverse
from django.core import serializers
from datetime import date
from herramientas import *
from models import *
from forms import *

# Create your views here.
def home(request):
    logeado = False
    u = None
    admin = False

    if request.user.is_authenticated:
        logeado = True
        u = request.user.perfil.nombreArtista
        if request.user.perfil.rol.is_admin():
            admin = True

    capsula = Capsulas.public.all()
    if len(capsula) is not 0:
         capsula =capsula[0]
    context = {
        'capsula' : capsula,
        'logeado' : logeado,
        'usuario' : u,
        'admin' : admin,
        'user' : request.user
    }
    return render(request, 'inicio.html', context)

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
        'perfil': perfil,
        'limit' : limit + aumento,
        'total' : total
    }
    return render(request, 'perfil_list.html', context)

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
        'total' : total
    }
    return render(request, 'actividad_list.html', context)

@login_required
def actividad_user(request, username=''):
    user = get_object_or_404(User, username=username)
    if request.user == user:
        actividad = Actividad.public.filter(perfil=user.perfil)
    else:
        actividad = Actividad.public.all()

    context = {'actividad': actividad, 'perfil': user}
    return render(request, 'actividad_user.html', context)

@login_required
def actividad_to_authorize(request):
    limit = 10
    aumento = 10
    total = False

    if request.GET:
        limit=request.GET['limit']
        limit = int(limit)

    actividad = Actividad.objects.all()[:limit]

    if len(actividad) != limit:
        total = True

    context = {
        'actividad': actividad,
        'limit' : limit + aumento,
        'total' : total
    }
    return render(request, 'autorizar_evento.html', context)

class EventosDetailView(DetailView):
    model = Perfil

    def get_context_data(self, **kwargs):
        context = super(EventosDetailView, self).get_context_data(**kwargs)
        actividades = Actividad.objects.filter(perfil=context['object']).order_by('fechaRealizacion')
        context = {'actividad': actividades}
        return context

def perfil_create_p1(request):
    mensaje = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        try:
            User.objects.get(username=username)
            mensaje = 'El nombre de usuario ya existe'
            form = UsuarioForm()

        except ObjectDoesNotExist :
            estado, mensaje = validar_password(username, password,password_confirm)
            if estado:
                request.session['username'] = username
                request.session['password'] = password
                return perfil_create_p2(request,user=True)
            form = UsuarioForm()
    else:
        form = UsuarioForm()

    context = {'form': form, 'mensaje': mensaje }
    return render(request, 'crear_perfil_p1.html', context)

def perfil_create_p2(request, user=None):
    print user
    if user != None:
        form = PerfilForm()
        context = {'form': form, 'create': True}
        return render(request, 'crear_perfil_p2.html', context)

    if request.method == 'POST':
        form = PerfilForm(data=request.POST)
        if form.is_valid():
            perfil = form.save(commit=False)

            img = request.FILES['imagen']
            img.name = renombrar_archivo(img.name,newName='perfil')
            perfil.imagen = img

            perfil.rol = get_object_or_404(Rol, nombreRol='Artista')

            username = request.session['username']
            password = request.session['password']
            nuevo_usuario = User.objects.create_user(username=username, email='xela@casacult.com', password=password)
            perfil.user = nuevo_usuario

            perfil.save()

            reescalar_imagen(perfil.imagen.path,perfil.imagen.path)

            del request.session['username']
            del request.session['password']

            return mensaje(request, 'Usuario Creado Exitosamente')
    else:
        return HttpResponseRedirect(reverse('error'))

def perfil(request, username=''):
    user = get_object_or_404(User, username=username)
    perfil = user.perfil
    is_owner = False

    if request.user == user:
        is_owner = True

    conteo = request.session.get('conteo' + username,False)
    if conteo == False and is_owner == False:
        perfil.visitas = perfil.visitas + 1
        perfil.save()
        request.session['conteo' + username] = True
        print False



    context = {
        'perfil': perfil,
        'es_propietario': is_owner,
    }
    return render(request, 'mi_perfil.html', context)

@login_required
def perfil_edit(request, username=''):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = PerfilForm(instance=user.perfil, data=request.POST)
        if form.is_valid():
            print "si"
            #form.save(commit=False)
            form.save()
            return mensaje(request, 'Perfil Modificado Exitosamente')
    else:
        print "no"
        form = PerfilForm(instance=user.perfil)
    context = {'form': form, 'create': False}
    return render(request, 'crear_perfil_p2.html', context)

@login_required
def actividad_create(request,username=''):
    if request.method == 'POST':
        form = ActividadForm(data=request.POST)
        if form.is_valid():
            actividad = form.save(commit=False)
            actividad.fechaPublicacion = date.today()

            img = request.FILES['imagen']
            img.name = renombrar_archivo(img.name,newName='actividad')
            actividad.imagen = img

            actividad.save()
            actividad.perfil.add(request.user.perfil)

            form.save_m2m()

            reescalar_imagen(actividad.imagen.path,actividad.imagen.path)

            return mensaje(request, 'Actividad Creada Exitosamente')
    else:
        form = ActividadForm()

    context = {'form': form, 'create': True}
    return render(request, 'crear_actividad.html', context)

@login_required
def capsula_create(request):
    if request.user.perfil.rol.is_admin() != True:
        return HttpResponseRedirect(reverse('error'))

    if request.method == 'POST':
        form = CapsulaForm(data=request.POST)
        if form.is_valid():
            capsula = form.save(commit=False)
            capsula.user = request.user
            capsula.save()
            return mensaje(request, 'Capsula Creada Exitosamente')
    else:
        form = CapsulaForm()

    context = {'form': form, 'create': True}
    return render(request, 'capsulas.html', context)

@login_required
def editar_capsula(request, pk = ''):
    capsula = get_object_or_404(Capsulas, pk=pk)
    if request.method == 'POST':
        form = CapsulaForm(instance=capsula, data=request.POST)
        if form.is_valid():
            form.save()
            return mensaje(request, 'Capsula Modificada Exitosamente')
    else:
        form = CapsulaForm(instance=capsula)
    context = {'form': form, 'create': False}
    return render(request, 'capsulas,html', context)

@login_required
def capsula_list(request):
    if request.user.perfil.rol.is_admin() != True:
        return HttpResponseRedirect(reverse('error'))

    limit = 20
    aumento = 20
    total = False

    if request.GET:
        limit=request.GET['limit']
        limit = int(limit)

    capsulas = Capsulas.objects.all()[:limit]

    if len(capsulas) != limit:
        total = True

    context = {
        'capsulas' : capsulas,
        'limit' : limit + aumento,
        'total' : total
    }
    return render(request, 'capsula_list.html', context)

@login_required
def administracion(request):

    if request.user.perfil.rol.is_admin() != True:
        return HttpResponseRedirect(reverse('error'))

    u = request.user.perfil.nombreArtista
    context = {
        'usuario' : u,
        }
    return render(request, 'Admi.html', context)

def ingresar(request):
    next = ""
    error = False

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home:perfil',kwargs={'username': request.user.username,}))

    if request.GET:
        next = request.GET['next']
        print next

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.perfil.autorizado == True:
                login(request, user)
                if next == "":
                    return HttpResponseRedirect(reverse('home:home'))
                else:
                    return HttpResponseRedirect(next)
            else:
                return mensaje(request, 'Tu usuario aun no ha sido autorizado...')
        else:
            error = True
            form = LoginForm()
    else:
        form = LoginForm()

    context = {'form': form, 'create': True, 'next':next, 'error':error,}
    return render(request, 'login.html', context)

@login_required
def cerrar_sesion(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect(reverse('home:home'))

def error(request):
    return render(request, 'error.html')

def actividad_detail(request, username='', id=''):
    logeado = False
    u = None
    admin = False
    actividad = Actividad.objects.get(id=int(id))

    if actividad.perfil.get().user.username != username:
        return HttpResponseRedirect(reverse('error'))

    if request.user.is_authenticated:
        logeado = True
        u = request.user.username
        if request.user.perfil.rol.is_admin():
            admin = True

    conteo = request.session.get('conteo' + id, False)
    if conteo == False:
        actividad.visitas = actividad.visitas + 1
        actividad.save()
        request.session['conteo' + id] = True
        print False


    context = {
        'logeado' : logeado,
        'usuario' : u,
        'admin' : admin,
        'actividad': actividad,
    }
    return render(request, 'detalle_actividad.html', context)

def mensaje(request, mensaje=''):
    if mensaje == None:
        return HttpResponseRedirect(reverse('error'))

    context={
        'mensaje':mensaje,
    }
    return render(request, 'mensaje.html', context)

@login_required
def actividad_authorize(request, id=''):
    actividad = Actividad.objects.get(id=int(id))
    #print id
    actividad.autorizado = 1
    actividad.save()

    return HttpResponseRedirect(reverse('home:home'))
