from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from .models import Perfil, Actividad
from .forms import PerfilForm, ActividadForm
# Create your views here.

def perfil_list(request):
    perfil = Perfil.public.all()
    context = {'perfil': perfil}
    return render(request, 'polls/perfil_list.html', context)

def actividad_list(request):
    actividad = Actividad.public.all()
    context = {'actividad': actividad}
    return render(request, 'polls/actividad_list.html', context)

def actividad_user(request, username):
    user = get_object_or_404(Perfil, username=nombreArtista)
    if request.user == user:
        actividad = user.perfil.all()
    else:
        actividad = Perfil.public.filter(perfil__username=nombreArtista)
    context = {'perfil': actividad, 'perfil': user}
    return render(request, 'polls/actividad_user.html', context)

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
    return reder(request, 'polls/form.html', context)

def perfil_edit(request, pk):
    perifl = get_object_or_404(Perfil, pk=pk)
    if request.method == 'POST':
        form = PerfilForm(instance=perfil, data=request.POST)
        if form.is_valid():
            form.save()
    else:
        form = PerfilForm(instance=perfil)
    context = {'form': form, 'create': False}
    return render(request, 'polls/form.html', context)

def actividad_create(request):
    if request.method == 'POST':
        form = ActividadForm(data=request.POST)
        if form.is_valid():
            actividad = form.save(commit=False)
            actividad.save()
            form.save_m2m()
    else:
        form = ActividadForm()
    context = {'form': form, 'create': True}
    return reder(request, 'polls/form.html', context)
