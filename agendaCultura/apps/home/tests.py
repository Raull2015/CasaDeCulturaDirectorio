from django.test import TestCase, RequestFactory
from django.urls import reverse
from datetime import date


from views import *
from models import *
from herramientas import *
# Create your tests here.

class CategoriaTest(TestCase):
    pass

class RolTest(TestCase):
    def setUp(self):
        self.admin = Rol.objects.create(nombreRol='Administrador',descripcion='nanana')
        self.artista = Rol.objects.create(nombreRol='Artista',descripcion='nonono')

    def test_is_admin(self):
        self.assertEqual(True, self.admin.is_admin() )
        self.assertEqual(False, self.artista.is_admin() )

    def test_is_artista(self):
        self.assertEqual(False, self.admin.is_artista() )
        self.assertEqual(True, self.artista.is_artista() )

class PerfilTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='yolo', email='yolo@gmail.com', password='ultrasecreto')
        rol = Rol.objects.create(nombreRol='Administrador',descripcion='nanana')

        self.perfil = Perfil.objects.create(nombreArtista= 'mcBeans', nombreReal='Juanito', sexo=0, fechaNacimiento='1995-01-01',
                                            telefono='12345678',email='yolo@gmail.com',descripcion='nel prro',fechaRegistro=date.today(),
                                            visitas=100,autorizado=1, rol=rol, user=user)

    def test_autorizados(self):
        listaPerfiles = Perfil.public.all()
        self.assertEqual(1,len(listaPerfiles))
        self.perfil.autorizado = 0
        self.perfil.save()
        listaPerfiles = Perfil.public.all()
        self.assertQuerysetEqual([],listaPerfiles)


class ActividadTest(TestCase):
    def setUp(self):
        self.actividad = Actividad.objects.create(nombre='Concierto', lugar='xela', fechaRealizacion='2016-11-11', hora='22:00',
                                                  descripcion='lalala', fechaPublicacion=date.today(), visitas=100, autorizado=1)

    def test_autorizados(self):
        listaActividades = Actividad.public.all()
        self.assertEqual(1,len(listaActividades))

        self.actividad.autorizado = 0
        self.actividad.save()
        listaActividades = Perfil.public.all()
        self.assertQuerysetEqual([],listaActividades)

class ComentarioTest(TestCase):
    pass

class CapsulaTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='prro', email='yolo2@gmail.com', password='ultrasecreto')
        self.capsula = Capsulas.objects.create(fechaPublicacion=date.today(),texto='glen se muere', usuario=user)

    def test_capsula_de_hoy(self):
        cap = Capsulas.public.all()[0]
        self.assertEqual(self.capsula.fechaPublicacion, cap.fechaPublicacion)

class HomeViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='nub', email='yolo3@gmail.com', password='ultrasecreto')
        rol = Rol.objects.create(nombreRol='Administrador',descripcion='nanana')

        Perfil.objects.create(nombreArtista= 'mcBeans', nombreReal='Juanito', sexo=0, fechaNacimiento='1995-01-01',
                             telefono='12345678',email='yolo@gmail.com',descripcion='nel prro',fechaRegistro=date.today(),
                             visitas=100,autorizado=1, rol=rol, user=self.user)

    def test_home_vista_sesion(self):
        request = self.factory.get('/home/')
        request.user = self.user

        response = home(request)
        result = response.content.find('Iniciar Sesion')
        self.assertNotEqual(-1, result)

class usernameTest(TestCase):
    def setUp(self):
        self.username1 = 'usuario1'
        self.username2 = '@wwwwww'
        self.username3 = '_wwwwww'
        self.username4 = '-wwwwww'

    def test_caracteres_nombres(self):
        result1, mensaje = validar_password(self.username1, '12345678', '12345678')
        result2, mensaje = validar_password(self.username2, '12345678', '12345678')
        result3, mensaje = validar_password(self.username3, '12345678', '12345678')
        result4, mensaje = validar_password(self.username4, '12345678', '12345678')

        self.assertEqual(True, result1)
        self.assertEqual(False, result2)
        self.assertEqual(False, result3)
        self.assertEqual(False, result4)
