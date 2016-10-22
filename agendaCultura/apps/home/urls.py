#urls de app home
from django.conf.urls import include, url
from views import index

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^user/(?P<username>[-\w]+)/$', 'polls.views.actividad_user',
        name='polls_actividad_user'),

    url(r'^$', 'polls.views.perfil_list', name='polls_perfil_list'),
]
