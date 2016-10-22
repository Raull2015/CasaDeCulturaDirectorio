from django.shortcuts import render, redirect
from django.http import HttpResponse
from models
# Create your views here.

def home(request):

    context = {

    }
    return render(request, 'home/inicio.html', context)
