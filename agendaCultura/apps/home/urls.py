#urls de app home
from django.conf.urls import include, url
from views import *

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'(?P<username>[-\w]+)/evento/(?P<id>[\d]+)/editar/$', anadir_imagen, name='anadir_imagen'),
    url(r'(?P<id>[\d]+)/comentar/$', comentarios, name='comentar'),
    url(r'confirmar_registro/$', confirmar_registro, name='confirmar_registro'),
    url(r'ayuda/$', ayuda, name='ayuda'),
    url(r'informacion/$', informacion , name='informacion'),
    url(r'^buscar/artista/$', buscar_artista, name='buscar_artista'),
    url(r'(?P<id>[\d]+)/categoria/$', categoria, name='categoria'),
    url(r'confirmar_actividad/$', confirmar_actividad, name='confirmar_actividad'),
    url(r'artistas/$', perfil_list, name='artistas'),
    url(r'categorias/$', categoria_list, name='categorias'),
    #url(r'registro/p2/$', perfil_create_p2, name='crear_perfil_p2'),
    url(r'registro/$', perfil_create_p1, name='crear_perfil_p1'),
    url(r'(?P<username>[-\w]+)/evento/(?P<id>[\d]+)$', actividad_detail, name='detalle_evento'),
    url(r'(?P<username>[-\w]+)/misEventos/$', actividad_user, name='actividad_user'),
    url(r'eventos/$', actividad_list, name='eventos'),
    url(r'(?P<username>[-\w]+)/editar/contrasenia/$', cambiar_contrasenia, name='cambiar_contrasenia'),
    url(r'(?P<username>[-\w]+)/editar/$', perfil_edit, name='editar_perfil'),
    url(r'(?P<username>[-\w]+)/crearEvento/$', actividad_create, name='crear_evento'),
    url(r'(?P<username>[-\w]+)/evento/(?P<id>[\d]+)/editar/$', anadir_colaborador, name='anadir_colaborador'),
    url(r'(?P<username>[-\w]+)/$', perfil, name='perfil'),
]
