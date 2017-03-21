# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-13 15:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Actividad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('lugar', models.CharField(max_length=200)),
                ('fechaRealizacion', models.DateField(verbose_name='Fecha a realizar')),
                ('hora', models.TimeField(verbose_name='Hora de Realizacion')),
                ('descripcion', models.TextField(max_length=800)),
                ('imagen', models.ImageField(default='imgActividad/default.jpg', upload_to='imgActividad/')),
                ('fechaPublicacion', models.DateField(verbose_name='Fecha de publicacion')),
                ('puntuacion', models.IntegerField(default=0)),
                ('visitas', models.IntegerField(default=0)),
                ('autorizado', models.SmallIntegerField(default=0)),
            ],
            options={
                'ordering': ['-fechaRealizacion'],
                'verbose_name': 'actividad',
                'verbose_name_plural': 'actividades',
            },
        ),
        migrations.CreateModel(
            name='Capsulas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaPublicacion', models.DateField(verbose_name='Fecha de publicacion')),
                ('texto', models.TextField(max_length=225)),
                ('autorizado', models.SmallIntegerField(default=1)),
                ('imagen', models.ImageField(default='imgCapsula/default.jpg', upload_to='imgCapsula/')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'capsula',
                'verbose_name_plural': 'capsulas',
            },
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoria', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'categoria',
                'verbose_name_plural': 'categorias',
            },
        ),
        migrations.CreateModel(
            name='Comentarios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenido', models.TextField(max_length=200)),
                ('fechaComentario', models.DateField(verbose_name='Fecha del comentario')),
                ('actividad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Actividad')),
            ],
            options={
                'verbose_name': 'comentario',
                'verbose_name_plural': 'comentarios',
            },
        ),
        migrations.CreateModel(
            name='Imagenes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(default='imgActividad/default.jpg', upload_to='imgActividad/')),
                ('actividad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Actividad')),
            ],
            options={
                'verbose_name': 'imagen',
                'verbose_name_plural': 'imagenes',
            },
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreArtista', models.CharField(max_length=100, null=True)),
                ('nombreReal', models.CharField(max_length=65)),
                ('imagen', models.ImageField(default='imgPerfil/default.jpg', upload_to='imgPerfil/')),
                ('sexo', models.SmallIntegerField(default=0)),
                ('fechaNacimiento', models.DateField(verbose_name='Fecha de nacimiento')),
                ('telefono', models.CharField(max_length=16)),
                ('email', models.EmailField(max_length=254, verbose_name='Correo')),
                ('descripcion', models.CharField(max_length=200, null=True)),
                ('fechaRegistro', models.DateField(auto_now_add=True, verbose_name='Fecha de registro')),
                ('visitas', models.IntegerField(default=0)),
                ('autorizado', models.SmallIntegerField(default=0)),
                ('categoria', models.ManyToManyField(to='home.Categoria')),
            ],
            options={
                'ordering': ['-fechaRegistro'],
                'verbose_name': 'perfil',
                'verbose_name_plural': 'perfiles',
            },
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreRol', models.CharField(max_length=45)),
                ('descripcion', models.CharField(max_length=45)),
            ],
            options={
                'verbose_name': 'rol',
                'verbose_name_plural': 'roles',
            },
        ),
        migrations.CreateModel(
            name='VisitasActividad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(default=0)),
                ('fecha', models.DateField()),
                ('actividad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Actividad')),
            ],
            options={
                'verbose_name': 'visitactividad',
                'verbose_name_plural': 'visitasactividades',
            },
        ),
        migrations.CreateModel(
            name='VisitasPerfil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(default=0)),
                ('fecha', models.DateField()),
                ('perfil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Perfil')),
            ],
            options={
                'ordering': ['-fecha'],
                'verbose_name': 'visitaperfil',
                'verbose_name_plural': 'visitasperfiles',
            },
        ),
        migrations.AddField(
            model_name='perfil',
            name='rol',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Rol'),
        ),
        migrations.AddField(
            model_name='perfil',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='actividad',
            name='categoria',
            field=models.ManyToManyField(to='home.Categoria'),
        ),
        migrations.AddField(
            model_name='actividad',
            name='perfil',
            field=models.ManyToManyField(db_index=True, to='home.Perfil'),
        ),
    ]
