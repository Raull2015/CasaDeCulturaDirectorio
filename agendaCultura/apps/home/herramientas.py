# -*- coding: utf-8 -*-
import os
from PIL import Image
import numpy as np
import plotly.offline as py
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

        ruta = GenGraficos.getRuta()
        fig = {
            'data' : [{'labels': etiquetas,
                        'values' : valores,
                        'type':'pie'}],
            'layout':{'title':titulo}
        }
        return py.plot(fig, include_plotlyjs=False, output_type='div',show_link=False)#rtua de imagen guardada

    def generoArtistasReg(self, fechaInicio = None, fechaFin = None):
        valores = np.array([ Perfil.objects.filter(sexo=0,fechaRegistro__range=(fechaInicio,fechaFin)).count(),
                    Perfil.objects.filter(sexo=1,fechaRegistro__range=(fechaInicio,fechaFin)).count()])
        etiquetas = [str('Mujeres %.2f' % (float(valores[0])/valores.sum()*100)) + '%',str('Hombres %.2f' % (float(valores[0])/valores.sum()*100)) + '%']
        titulo = 'Numero de Hombres y Mujeres registrados desde ' + fechaInicio + ' hasta ' + fechaFin
        return valores, etiquetas, titulo

    def edadesArtistasReg(self,fechaInicio = None, fechaFin = None, rangoEdades=5 ) :
        pass

    def generarGrafico(self, tipoGrafico, tipoEstadistica, **kwargs):

        valores, etiquetas, titulo = tipoEstadistica(**kwargs)
        return tipoGrafico(valores,etiquetas,titulo)




def pruebas():
    test = GenGraficos()
    test.generarGrafico(test.graficaPie,test.generoArtistasReg,fechaInicio='2016-01-01',fechaFin='2016-11-20')


"""def graficaBarra():
        prima = 600 + np.random.randn(5) * 10  # Valores inventados para la prima de riesgo
        fechas = (dt.date.today() - dt.timedelta(5)) + dt.timedelta(1) * np.arange(5) # generamos las fechas de los últimos cinco días
        plt.axes((0.1, 0.3, 0.8, 0.6))  # Definimos la posición de los ejes
        plt.bar(np.arange(5), prima)  # Dibujamos el gráfico de barras
        plt.ylim(550,650)  # Limitamos los valores del eje y al range definido [450, 550]
        plt.title('prima de riesgo')  # Colocamos el título
        plt.xticks(np.arange(5), fechas, rotation = 45)  # Colocamos las etiquetas del eje x, en este caso, las fechas"""
