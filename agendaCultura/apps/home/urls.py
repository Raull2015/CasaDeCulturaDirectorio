#urls de app home
from django.conf.urls import include, url
from views import home

urlpatterns = [
    url(r'^$', home, name='index'),
]
