#urls de app home
from django.conf.urls import include, url
from views import *
from .views import EventosDetailView

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'artistas/$', perfil_list, name='artistas'),
    url(r'registro/p2/$', perfil_create_p2, name='crear_perfil_p2'),
    url(r'registro/$', perfil_create_p1, name='crear_perfil_p1'),
    #url(r'(?P<pk>[\d]+)/$', EventosDetailView.as_view(), name='mis_actividades'),
    url(r'(?P<username>[-\w]+)/crearEvento/$', actividad_create, name='crear_evento'),
    url(r'(?P<username>[-\w]+)/evento/(?P<id>[\d]+)$', actividad_detail, name='detalle_evento'),
    url(r'(?P<username>[-\w]+)/eventos/$', actividad_user, name='actividad_user'),
    url(r'(?P<username>[-\w]+)/editar/$', perfil_edit, name='editar_perfil'),
    url(r'eventos/$', actividad_list, name='eventos'),
    url(r'(?P<username>[-\w]+)/$', perfil, name='perfil'),
    #url(r'^buscar/$', search_artista, name='buscar'),
    #url(r'admin/eventos/$', actividad_to_authorize, name='actividad_pendiente'),
]
