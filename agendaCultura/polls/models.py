from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Categoria(models.Model):
    categoria = models.CharField(max_length=100)

class Perfil(models.Model):
    nombreArtista = models.CharField(max_length=100)
    nombreReal = models.CharField(max_length=65)
    imagen = models.CharField(max_length=100)
    sexo = models.SmallIntegerField(default=0)
    fechaNacimiento = models.DateField('fecha nacimiento',None, True)
    telefono = models.CharField(max_length=16)
    email= models.EmailField('Correo invalido')
    descripcion = models.CharField(max_length=200)
    fechaRegistro = models.DateField('fecha registro', None, True)
    visitas = models.IntegerField(default=0)
    autorizado = models.SmallIntegerField(default=0)
    categoria = models.ManyToManyField(Categoria)

    class Meta:
        verbose_name = 'pefil'
        verbose_name_plural = 'perfiles'
        ordering = ['-fechaRegistro']

    def __str__(self):
        return self.nombreArtista

class Actividad(models.Model):
    nombre = models.CharField(max_length=200)
    lugar = models.CharField(max_length=200)
    fechaRealizacion = models.DateField('fecha realizacion')
    hora = models.TimeField()
    descripcion = models.TextField(max_length=800)
    imagen = models.CharField(max_length=100)
    fechaPublicacion = models.DateField('fecha publicacion')
    puntuacion = models.IntegerField(default=0)
    visitas = models.IntegerField(default=0)
    autorizado = models.SmallIntegerField(default=0)
    categoria = models.ManyToManyField(Categoria)
    perfil = models.ManyToManyField(Perfil)

    class Meta:
        verbose_name = 'actividad'
        verbose_name_plural = 'actividades'
        ordering = ['-fechaRealizacion']

    def __str__(self):
        return self.nombre

class Comentarios(models.Model):
    contenido = models.TextField(max_length=200)
    fechaComentario = models.DateField('fecha comentario')
    actividad = models.ForeignKey(Actividad)

class Rol(models.Model):
    nombreRol = models.CharField(max_length=45)
    descripcion = models.CharField(max_length=45)

    def __str__(self):
        return self.nombreRol

class Usuarios(models.Model):
    login = models.CharField(max_length=100)
    pwd = models.CharField(max_length=40)
    ultimaConexion = models.DateField('ultima conexion')
    perfil = models.ForeignKey(Perfil)
    rol = models.ForeignKey(Rol)

class Capsulas(models.Model):
    fechaPublicacion = models.DateField('fecha publicacion')
    texto = models.TextField(max_length=225)
    autorizado = models.SmallIntegerField(default=0)
    usuario = models.ForeignKey(Usuarios)



