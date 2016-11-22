# -*- coding: utf-8 -*-
import os
from PIL import Image
import numpy as np
import plotly.offline as py
import plotly.graph_objs as go
from models import *

def reescalar_imagen(img,output,height=300,width=400,ext='.png'):
    archivo_in, old_ext = os.path.splitext(img)
    archivo_out, new_ext = os.path.splitext(output)
    imagen = Image.open(img)


    old_width, old_height = imagen.size
    #width = int((1.0 * old_width)/old_height * height)
    new_img = imagen.resize((width, height), Image.ANTIALIAS)    # best down-sizing filter

    if new_ext == None:
        new_ext = ext

    new_img.save(archivo_out + new_ext)

    print "Imagen rescalada a ", height , " * ", width

def renombrar_archivo(currentName,newName="archivo"):
    archivo, old_ext = os.path.splitext(currentName)
    return newName + old_ext

def validar_password(username, password, password_confirm):

    car_prohibidos = {'-','_','@',':'}
    for c in car_prohibidos:
        if username.find(c) != -1:
            return False, 'El nombre de usuario no puede tener el caracter' + c

    if len(username) < 4:
        return False, 'El nombre de usuario debe tener almenos 4 caracteres'
    if password != password_confirm:
        return False, 'Las contraseñas no coinciden'
    if len(password) < 8:
        return False, 'La contraseña debe tener almenos 8 caracteres'

    return True, None


class GenGraficos():

    ruta = 'imagen'
    noImagen = 0

    @classmethod
    def getRuta(self):
        self.noImagen = self.noImagen + 1
        return self.ruta + str(self.noImagen)

    def graficaPie(self, valores, etiquetas, titulo):

        data = [go.Pie(labels=etiquetas,values = valores)]
        layout = go.Layout(title=titulo)
        fig = go.Figure(data=data, layout=layout)
        return fig

    def graficaBarra(self, valores, etiquetas, titulo):

        data = [go.Bar(x=etiquetas,
                       y=valores,
                       name=titulo,
                       marker=dict(color='rgb(' + str(49 + 26) + ',' + str(130) + ',' + str(189) + ')'))]
        layout = go.Layout( xaxis=dict(tickangle=-45),
                            barmode='group',
                            title= titulo)
        return go.Figure(data=data, layout=layout)


    def graficaLinea(self, valores, etiquetas, titulo):
        data = [go.Scatter(x=etiquetas,
                           y=valores)]
        layout = go.Layout(title=titulo)

        return go.Figure(data=data,layout=layout)


    def generoArtistasReg(self, fechaInicio = None, fechaFin = None):
        valores = [ Perfil.objects.filter(sexo=0,fechaRegistro__range=(fechaInicio,fechaFin)).count(),
                    Perfil.objects.filter(sexo=1,fechaRegistro__range=(fechaInicio,fechaFin)).count()]
        etiquetas = ['Mujeres' ,'Hombres']
        titulo = 'Numero de Hombres y Mujeres registrados desde ' + fechaInicio + ' hasta ' + fechaFin

        return valores, etiquetas, titulo

    def artistasPorCategoria(self):
        valores = []
        etiquetas = []
        rol = Rol.objects.get(nombreRol = 'Artista')
        for c in Categoria.objects.all():
            valores.append(Perfil.public.filter(rol = rol , categoria=c).count())
            etiquetas.append(c.categoria)

        titulo = 'Numero de Artistas Registrados por Categoria'
        return valores, etiquetas, titulo

    def eventosPorCategoria(self):
        valores = []
        etiquetas = []
        for c in Categoria.objects.all():
            valores.append(Actividad.public.filter(categoria=c).count())
            etiquetas.append(c.categoria)

        titulo = 'Numero de Eventos realizados por Categoria'
        return valores, etiquetas, titulo

    def artistasVisitas(self, limite=10):
        valores = []
        etiquetas = []
        rol = Rol.objects.get(nombreRol = 'Artista')
        for c in Perfil.public.filter(rol = rol).order_by('visitas')[:limite]:
            valores.append(c.visitas)
            etiquetas.append(c.nombreArtista)

        titulo = "Artistas Mas Visitados"
        return valores, etiquetas, titulo

    def eventosVisitas(self, limite = 10):
        valores = []
        etiquetas = []
        for c in Perfil.public.all().order_by('visitas')[:limite]:
            valores.append(c.visitas)
            etiquetas.append(c.nombreArtista)
            titulo = "Eventos Mas Vistos"
            return valores, etiquetas, titulo

    def generarGrafico(self, tipoGrafico, tipoEstadistica, **kwargs):
        valores, etiquetas, titulo = tipoEstadistica(**kwargs)
        fig = tipoGrafico(valores,etiquetas,titulo)
        return py.plot(fig, include_plotlyjs=False, output_type='div',show_link=False)#ruta de imagen guardada
