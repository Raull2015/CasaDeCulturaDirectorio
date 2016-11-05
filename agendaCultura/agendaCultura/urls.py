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

urlpatterns = [
    url(r'^static/(?P<path>.*)$', serve, {
        'document_root': settings.STATIC_ROOT,
    }),
    url(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/', include(homeUrls, namespace='home')),
    #url(r'^artistas/', views.perfil_list),
    #url(r'^registro/$', views.perfil_create),
    url(r'^login/', views.ingresar, name='iniciar_sesion'),
    url(r'^logout/', views.cerrar_sesion, name='cerrar_sesion'),
    #url(r'^home/listaArtistas', views.perfil_list),
    #url(r'^home/listaEventos', views.actividad_list),
    #url(r'^home/perfil/crearActividad', views.actividad_create),
    #url(r'^administracion/capsulas/', views.capsula_create, name='capsula_create'),
    url(r'^administracion/capsula/(?P<pk>\d+)$', views.editar_capsula, name='editar_capsula'),
    url(r'^administracion/capsula/crear$', views.capsula_create, name='capsula_create'),
    url(r'^administracion/$', views.administracion, name='administracion'),
    url(r'^error/', views.error, name='error'),
    #url(r'^edit/', views.perfil_edit),
    #url(r'^user/(?P<username>[-\w]+)/$', views.actividad_user),
    #url(r'^edit/(?P<pk>\d+)/$', views.perfil_edit),
    url(r'^', views.home, name='default'),

]
