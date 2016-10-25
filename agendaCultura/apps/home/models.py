from __future__ import unicode_literals

from django.db import models
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
class PerfilManager(models.Manager):
    def get_queryset(self):
        qs = super(PerfilManager, self).get_queryset()
        return qs.filter(autorizado=1)

class ActividadManager(models.Manager):
    def get_queryset(self):
        qs = super(ActividadManager, self).get_queryset()
        return qs.filter(autorizado=1)

class CapsulaManager(models.Manager):
    def get_queryset(self):
        qs = super(CapsulaManager, self).get_queryset()
        return qs.filter(fechaPublicacion=date.today())


class Categoria(models.Model):
    categoria = models.CharField(max_length=100)

    def __str__(self):
        return self.categoria

    class Meta:
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'

class Rol(models.Model):
    nombreRol = models.CharField(max_length=45)
    descripcion = models.CharField(max_length=45)

    def __str__(self):
        return self.nombreRol

    def is_admin(self):
        if nombreRol == 'Administrador':
            return True

    def is_artista(self):
        if nombreRol == 'Artista':
            return True

    class Meta:
        verbose_name = 'rol'
        verbose_name_plural = 'roles'

class Perfil(models.Model):
    nombreArtista = models.CharField(max_length=100)
    nombreReal = models.CharField(max_length=65)
    imagen = models.CharField(max_length=100)
    sexo = models.SmallIntegerField(default=0)
    fechaNacimiento = models.DateField('Fecha de nacimiento')
    telefono = models.CharField(max_length=16)
    email= models.EmailField('Correo')
    descripcion = models.CharField(max_length=200)
    fechaRegistro = models.DateField('Fecha de registro')
    visitas = models.IntegerField(default=0)
    autorizado = models.SmallIntegerField(default=0)
    categoria = models.ManyToManyField(Categoria)

    rol = models.ForeignKey(Rol)
    user =  models.OneToOneField(User, on_delete=models.CASCADE)

    objects = models.Manager()
    public = PerfilManager()

    class Meta:
        verbose_name = 'perfil'
        verbose_name_plural = 'perfiles'
        ordering = ['-fechaRegistro']

    def __str__(self):
        return self.nombreArtista

class Actividad(models.Model):
    nombre = models.CharField(max_length=200)
    lugar = models.CharField(max_length=200)
    fechaRealizacion = models.DateField('Fecha a realizar')
    hora = models.TimeField('Hora de Realizacion')
    descripcion = models.TextField(max_length=800)
    imagen = models.CharField(max_length=100)
    fechaPublicacion = models.DateField('Fecha de publicacion')
    puntuacion = models.IntegerField(default=0)
    visitas = models.IntegerField(default=0)
    autorizado = models.SmallIntegerField(default=0)
    categoria = models.ManyToManyField(Categoria)
    perfil = models.ManyToManyField(Perfil)

    objects = models.Manager()
    public = ActividadManager()

    class Meta:
        verbose_name = 'actividad'
        verbose_name_plural = 'actividades'
        ordering = ['-fechaRealizacion']

    def __str__(self):
        return self.nombre


class Comentarios(models.Model):
    contenido = models.TextField(max_length=200)
    fechaComentario = models.DateField('Fecha del comentario')
    actividad = models.ForeignKey(Actividad)

    def __str__(self):
        return self.contenido

    class Meta:
        verbose_name = 'comentario'
        verbose_name_plural = 'comentarios'

"""
class Usuarios(models.Model):
    login = models.CharField(max_length=100)
    pwd = models.CharField(max_length=40)
    ultimaConexion = models.DateField('Ultia conexion')
    perfil = models.ForeignKey(Perfil)
    rol = models.ForeignKey(Rol)

    def __str__(self):
        return self.login
"""

class Capsulas(models.Model):
    fechaPublicacion = models.DateField('Fecha de publicacion')
    texto = models.TextField(max_length=225)
    autorizado = models.SmallIntegerField(default=0)
    usuario = models.ForeignKey(User)

    public = CapsulaManager()

    def __str__(self):
        return self.texto

    class Meta:
        verbose_name = 'capsula'
        verbose_name_plural = 'capsulas'
