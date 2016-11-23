# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from .models import Perfil, Actividad, Capsulas, Categoria

class PerfilForm(ModelForm):
    class Meta:
        model = Perfil
        fields = (
            'nombreArtista',
            'nombreReal',
            'imagen',
            'sexo',
            'fechaNacimiento',
            'telefono',
            'email',
            'descripcion',
            'categoria',
            )
        label = {
            'nobmreArtista': 'Nombre artistico:',
            'nombreReal': 'Nombre real:',
            'imagen': 'Insertar imagen',
            'sexo': 'Genero:',
            'fechaNacimiento':'Fecha de nacimiento:',
            'telefono':'Telfeno:',
            'email': 'Correo electronico:',
            'descripcion': 'Descripcion (opcional):',
        }
        exclude = ('visitas', 'autorizado', 'fechaRegistro')
        CHOICES = (('1', 'Masculino',), ('0', 'Femenino',))
        widgets = {
            'fechaNacimiento': forms.SelectDateWidget(years=range(1900,2001)),
            'sexo': forms.RadioSelect( choices=CHOICES)#'imagen': forms.FileInput(),
        }

class ActividadForm(ModelForm):
    class Meta:
        model = Actividad
        fields = (
            'nombre',
            'lugar',
            'fechaRealizacion',
            'hora',
            'descripcion',
            'imagen',
            'categoria',
        )
        label = {
            'nombre': 'Nombre del evento:',
            'lugar': 'Lugar:',
            'fechaRealizacion': 'Fecha a realizar el evento:',
            'hora': 'Hora:',
            'descripcion': 'Descripcion:',
            'imagen': 'Imagen',
            'categoria':'Seleccionar categoria:',
        }
        widgets = {
            'fechaRealizacion': forms.SelectDateWidget(),
            'hora': forms.TimeInput(),
            #'imagen' : forms.ClearableFileInput(),
        }

class CapsulaForm(ModelForm):
    class Meta:
        model = Capsulas
        fields = (
            'texto',
            'fechaPublicacion',
        )
        label = {
            'texto': 'Texto:',
            'fechaPublicacion': 'Fecha a publicarse:',
        }
        exclude = ('autorizado','usuario')
        widgets = {
            'fechaPublicacion': forms.SelectDateWidget(years=range(2015,2020)),
            #'texto': forms.
        }

class LoginForm(forms.Form):
    username = forms.CharField(widget= forms.TextInput(attrs={'class': 'form-control'}), label = 'Usuario')
    password = forms.CharField(widget = forms.PasswordInput(attrs={'class': 'form-control'}) , label = 'Contraseña')

class UsuarioForm(forms.Form):
    username = forms.CharField(widget= forms.TextInput(attrs={'class': 'form-control'}), label = 'Usuario')
    password = forms.CharField(widget = forms.PasswordInput(attrs={'class': 'form-control'}) , label = 'Contraseña')
    password_confirm = forms.CharField(widget = forms.PasswordInput(attrs={'class': 'form-control'}) , label = 'Repite Contraseña')
