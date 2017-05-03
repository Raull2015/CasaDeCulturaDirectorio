# -*- coding: utf-8 -*-
from django.core.mail import EmailMessage
import os
from PIL import Image
from datetime import date
import numpy as np
import plotly.offline as py
import plotly.graph_objs as go
from models import Perfil, Rol, Actividad, Capsulas, Categoria, Publicidad, ImagenesHome

def reescalar_imagen(img,output,height=260,width=370,ext='.png'):
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

    def getTipoEstadistica(self, tipo):
        tipos = { 'generoArtistas' : self.generoArtistasReg,
                  'categoriaArtistas': self.artistasPorCategoria,
                  'categoriaEventos': self.eventosPorCategoria,
                  'visitasArtistas': self.artistasVisitas,
                  'visitasEventos': self.eventosVisitas,}

        return tipos.get(tipo,None)

    def getTipoGrafica(self, tipo):
        tipos = { 'Pie' : self.graficaPie,
                  'Barras': self.graficaBarra,
                  'Linea': self.graficaLinea,}

        return tipos.get(tipo,None)

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


    def generoArtistasReg(self, fechaInicio = '2016-01-01', fechaFin = None):
        if fechaFin == None:
            fechaFin = str(date.today())

        valores = [ Perfil.objects.filter(sexo=0,fechaRegistro__range=(fechaInicio,fechaFin)).count(),
                    Perfil.objects.filter(sexo=1,fechaRegistro__range=(fechaInicio,fechaFin)).count()]
        etiquetas = ['Mujeres' ,'Hombres']
        titulo = 'Porcentaje de artistas registrados por genero desde ' + fechaInicio + ' hasta ' + fechaFin

        return valores, etiquetas, titulo

    def artistasPorCategoria(self, fechaInicio = '2016-01-01', fechaFin = None):
        if fechaFin == None:
            fechaFin = str(date.today())
        valores = []
        etiquetas = []
        rol = Rol.objects.get(nombreRol = 'Artista')
        for c in Categoria.objects.all():
            valores.append(Perfil.public.filter(rol = rol , categoria=c, fechaRegistro__range=(fechaInicio,fechaFin)).count())
            etiquetas.append(c.categoria)

        titulo = 'Porcentaje de Artistas Registrados por Categoria desde ' + fechaInicio + ' hasta ' + fechaFin
        return valores, etiquetas, titulo

    def eventosPorCategoria(self, fechaInicio = '2016-01-01', fechaFin = None):
        if fechaFin == None:
            fechaFin = str(date.today())
        valores = []
        etiquetas = []
        for c in Categoria.objects.all():
            valores.append(Actividad.public.filter(categoria=c,fechaRealizacion__range=(fechaInicio,fechaFin)).count())
            etiquetas.append(c.categoria)

        titulo = 'Porcentaje de Eventos realizados por Categoria desde ' + fechaInicio + ' hasta ' + fechaFin
        return valores, etiquetas, titulo

    def artistasVisitas(self, limite=10):
        valores = []
        etiquetas = []
        rol = Rol.objects.get(nombreRol = 'Artista')
        for c in Perfil.public.filter(rol = rol).order_by('visitas')[:limite]:
            valores.append(c.visitas)
            etiquetas.append(c.nombreArtista)

        titulo = "Top " + str(limite) + " artistas mas vistos"
        return valores, etiquetas, titulo

    def eventosVisitas(self, limite = 10):
        valores = []
        etiquetas = []
        for c in Actividad.public.all().order_by('-visitas')[:limite]:
            valores.append(c.visitas)
            etiquetas.append(c.nombre)

        titulo = "Top " + str(limite) + " eventos mas vistos"
        return valores, etiquetas, titulo

    def generarGrafico(self, tipoGrafico, tipoEstadistica, **kwargs):
        valores, etiquetas, titulo = tipoEstadistica(**kwargs)
        fig = tipoGrafico(valores,etiquetas,titulo)
        return py.plot(fig, include_plotlyjs=False, output_type='div',show_link=False)#ruta de imagen guardada

def infoHome(request, context):
    logeado = False
    u = None
    admin = False
    categorias = []

    if request.user.is_authenticated:
        logeado = True
        u = request.user.perfil.nombreArtista
        if request.user.perfil.rol.is_admin():
            admin = True

    categorias = Categoria.objects.all()[:5]
    imagen = ImagenesHome.objects.get(id=1)

    publicidadI = Publicidad.objects.filter(visible=True)[:2]
    publicidadD = Publicidad.objects.filter(visible=True)[2:4]

    info = {
        'H_logeado' : logeado,
        'H_nombre_usuario' : u,
        'H_admin' : admin,
        'H_user' : request.user.username,
        'H_categorias' : categorias,
        'H_publicidadD' : publicidadD,
        'H_publicidadI' : publicidadI,
        'H_imagen' : imagen
    }
    info.update(context)
    return info

def EnviarCorreo(opcion,idPerfil, idEvento):

    administradores = Perfil.objects.filter(rol=Rol.objects.get(nombreRol="Administrador"))
    if opcion == 1:
        asunto = 'Nueva solicitud de inscripción'
        perfil = Perfil.objects.get(id=idPerfil)
        mensaje ='El(La) artista ' + str(perfil.nombreArtista) \
        + ' se desea unir a Calendart.'
        for admin in administradores:
            print admin.nombreReal + "  " +str(admin.id)
            mail = EmailMessage(asunto, mensaje, to = [admin.email])
            mail.send()

    else:
        asunto = 'Nueva solicitud de evento'
        actividad = Actividad.objects.get(id=idEvento)
        perfil = Perfil.objects.get(id=idPerfil)
        mensaje ='El(La) artista ' + str(perfil.nombreArtista) \
        + ' desea crear el evento que lleva por título ' \
        + str(actividad.nombre) + "."
        for admin in administradores: 
            mail = EmailMessage(asunto, mensaje, to = [admin.email])
            mail.send()


