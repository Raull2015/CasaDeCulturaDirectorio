from django.forms import ModelForm
from .models import Perfil, Actividad

class PerfilForm(ModelForm):
    class Meta:
        model = Perfil
        exclude = ('visitas', 'autorizado')

class ActividadForm(ModelForm):
    class Meta:
        model = Actividad
        exclude = ('puntuacion', 'visitas', 'autorizado')
