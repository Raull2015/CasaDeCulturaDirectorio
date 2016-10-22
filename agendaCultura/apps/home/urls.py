#urls de app home
from django.conf.urls import include, url
from views import home

urlpatterns = [
    url(r'^$', home, name='home'),
    #url(r'^user/(?P<username>[-\w]+)/$', 'polls.views.actividad_user',
    #    name='polls_actividad_user'),
    #url(r'^$', 'polls.views.perfil_list', name='polls_perfil_list'),
]
