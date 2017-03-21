from django.contrib import admin
from models import *
# Register your models here.

class PerfilAdmin(admin.ModelAdmin):
    list_display = ('nombreArtista', 'nombreReal','imagen','sexo','fechaNacimiento','telefono','email','descripcion','fechaRegistro')
    list_filter = ('nombreArtista', 'visitas', 'autorizado')
    search_fields = ['nombreArtista', 'nombreReal']

#class ActividadAdmin(admin.ModelAdmin):
    #list_display = ('nombre', 'lugar', 'fechaRealizacion', 'hora', 'descripcion', 'imagen', 'fechaPublicacion')
    #list_filter = ('nombre', 'lugar', 'autorizado')
    #search_fields = ['nombre', 'lugar']

#class CategoriaAdmin(admin.ModelAdmin):
#    list_display = ('categoria')
#    list_filter = ('categoria')
#    search_fields = ('categoria')

admin.site.register(Perfil, PerfilAdmin)
admin.site.register(Categoria)
admin.site.register(Actividad)
admin.site.register(Capsulas)
admin.site.register(Rol)
admin.site.register(Imagenes)
admin.site.register(VisitasPerfil)
admin.site.register(VisitasActividad)


# Register your models here.
