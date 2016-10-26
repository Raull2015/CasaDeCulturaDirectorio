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
            'descripcion'
            )
        label = {
            'nobmreArtista': 'Nombre artistico:',
            'nombreReal': 'Nombre real:',
            'imagen': 'Insertar imagen',
            'sexo': 'Sexo:',
            'fechaNacimiento':'Fecha de nacimiento:',
            'telefono':'Telfeno:',
            'email': 'Correo electronico:',
            'descripcion': 'Descripcion (opcional):',
        }
        exclude = ('visitas', 'autorizado')
        widgets = {
            'fechaNacimiento': forms.SelectDateWidget(years={'1980','2000',}),
            'imagen': forms.FileInput(),
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
        exclude = ('fechaPublicacion','puntuacion', 'visitas', 'autorizado','perfil')
        widgets = {
            'fechaRealizacion': forms.SelectDateWidget(),
            'hora': forms.TimeInput(),
            'imagen' : forms.FileInput(),
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
            'fechaPublicacion': forms.SelectDateWidget(years='2016')
        }
class LoginForm(forms.Form):
    username = forms.CharField(widget= forms.TextInput(attrs={'class': 'form-control'}), label = 'Usuario')
    password = forms.CharField(widget = forms.PasswordInput(attrs={'class': 'form-control'}) , label = 'Contrasenia')
