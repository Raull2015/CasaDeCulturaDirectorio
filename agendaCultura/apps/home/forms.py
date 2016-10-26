from django.forms import ModelForm
from django import forms
from .models import Perfil, Actividad, Capsulas, Categoria

class PerfilForm(ModelForm):
    class Meta:
        model = Perfil
        exclude = ('visitas', 'autorizado')

class ActividadForm(ModelForm):
    class Meta:
        model = Actividad
        exclude = ('fechaPublicacion','puntuacion', 'visitas', 'autorizado','perfil')
        widgets = {
            'fechaRealizacion': forms.SelectDateWidget(),
            'hora': forms.TimeInput(),
            'imagen' : forms.FileInput(),
        }

class CapsulaForm(ModelForm):
    class Meta:
        model = Capsulas
        exclude = ('autorizado','usuario')

class LoginForm(forms.Form):
    username = forms.CharField(widget= forms.TextInput(attrs={'class': 'form-control'}), label = 'Usuario')
    password = forms.CharField(widget = forms.PasswordInput(attrs={'class': 'form-control'}) , label = 'Contrasenia')
