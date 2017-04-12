"""agendaCultura URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views
from django.core.urlresolvers import reverse_lazy
from django.views.static import serve
from apps.home import views
from apps.home import urls as homeUrls

handler404 = views.error
urlpatterns = [
    url(r'^static/(?P<path>.*)$', serve, {
        'document_root': settings.STATIC_ROOT,
    }),
    url(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/', include(homeUrls, namespace='home')),
    url(r'^login/$', views.ingresar, name='iniciar_sesion'),
    url(r'^login_page/$', views.ingresar_pagina, name='ingresar_pagina'),
    url(r'^logout/$', views.cerrar_sesion, name='cerrar_sesion'),
    url(r'administracion/evento/aceptado/(?P<id>[\d]+)$', views.actividad_authorize, name='autorizar_evento'),
    url(r'administracion/evento/rechazado/(?P<id>[\d]+)$', views.actividad_reject, name='rechazar_evento'),
    url(r'administracion/artista/aceptado/(?P<id>[\d]+)$', views.artista_authorize, name='autorizar_artista'),
    url(r'administracion/artista/rechazado/(?P<id>[\d]+)$', views.artista_reject, name='rechazar_artista'),
    url(r'administracion/capsula/(?P<pk>\d+)/$', views.editar_capsula, name='editar_capsula'),
    url(r'administracion/capsula/crear/$', views.capsula_create, name='crear_capsula'),
    url(r'administracion/capsula/$', views.capsula_list, name='ver_capsulas'),
    url(r'administracion/categorias/editar/(?P<id>[\d]+)/$', views.categoria_editar, name='editar_categoria'),
    url(r'administracion/categorias/crear/$', views.categoria_crear, name='crear_categoria'),
    url(r'administracion/categorias/$', views.categoria_admin, name='admin_categoria'),
    url(r'administracion/eventos/$', views.actividad_to_authorize, name='actividad_pendiente'),
    url(r'administracion/artistas/$', views.artista_to_authorize, name='artista_pendiente'),
    url(r'administracion/publicidad/editar/(?P<id>[\d]+)/$', views.publicidad_editar, name='editar_publicidad'),
    url(r'administracion/publicidad/$', views.publicidad_list, name='publicidad'),
    url(r'administracion/$', views.administracion, name='administracion'),
    url(r'^buscar/artista/$', views.search_artista, name='buscarA'),
    url(r'^buscar/evento/$', views.search_actividad, name='buscarE'),
    url(r'error/$', views.error, name='error'),
    url(r'estadisticas/$', views.estadisticas, name='estadisticas'),
    url(r'registrarse/$', views.registrarse_pagina, name='registrarse'),
    url(r'^', views.home, name='default'),
]
