from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import *

# Create your views here.

def home(request):

    capsula = Capsulas.public.all()
    if len(capsula) is not 0:
         capsula =capsula[0]
    context = {
        'capsula' : capsula
    }
    return render(request, 'inicio.html', context)

def perfil_list(request):
    perfil = Perfil.public.all()
    context = {'perfil': perfil}
    return render(request, 'artistas.html', context)

def actividad_list(request):
    actividad = Actividad.public.all()
    context = {'actividad': actividad}
    return render(request, 'actividades.html', context)

@login_required
def actividad_user(request, username):
    user = get_object_or_404(Perfil, username=nombreArtista)
    if request.user == user:
        actividad = user.perfil.all()
    else:
        actividad = Perfil.public.filter(perfil__username=nombreArtista)
    context = {'perfil': actividad, 'perfil': user}
    return render(request, 'home/actividad_user.html', context)

def perfil_create(request):
    if request.method == 'POST':
        form = PerfilForm(data=request.POST)
        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.save()
            form.save_m2m()
    else:
        form = PerfilForm()
    context = {'form': form, 'create': True}
    return reder(request, 'home/form.html', context)

@login_required
def perfil_edit(request, pk):
    perifl = get_object_or_404(Perfil, pk=pk)
    if request.method == 'POST':
        form = PerfilForm(instance=perfil, data=request.POST)
        if form.is_valid():
            form.save()
    else:
        form = PerfilForm(instance=perfil)
    context = {'form': form, 'create': False}
    return render(request, 'home/form.html', context)

@login_required
def actividad_create(request):
    if request.method == 'POST':
        form = ActividadForm(data=request.POST)
        if form.is_valid():
            print "formulario actividad valido"
            actividad = form.save(commit=False)
            actividad.save()
            form.save_m2m()
            HttpResponseRedirect('inicio/')
    else:
        form = ActividadForm()

    context = {'form': form, 'create': True}
    return render(request, 'crearActividad.html', context)

@login_required
def capsula_create(request):
    if request.user.perfil.rol.is_admin != True:
        return HttpResponseRedirect('/error/')

    if request.method == 'POST':
        form = CapsulaForm(data=request.POST)
        if form.is_valid():
            capsula = form.save(commit=False)
            capsula.save()
            form.save_m2m()
            HttpResponseRedirect('/home/perfil/')
    else:
        form = CapsulaForm()

    context = {'form': form, 'create': True}
    return render(request, 'capsulas.html', context)

def ingresar(request):
    next = ""

    if request.user.is_authenticated:
        return HttpResponseRedirect('/home/perfil/')

    if request.GET:
        next = request.GET['next']

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if next == "":
                    return HttpResponseRedirect('/home/')
                else:
                    return HttpResponseRedirect(next)
            else:
                #el usuario no esta activo
                pass
        else:
            return HttpResponseRedirect('/login/')
    else:
        form = LoginForm()

    context = {'form': form, 'create': True, 'next':next, }
    return render(request, 'login.html', context)
