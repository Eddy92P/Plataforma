# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib.auth.models import User
from apps.comunidad import apps
from django.contrib.auth.models import AbstractUser

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from django.db import models

from django.conf import settings

from django.utils.safestring import mark_safe

class User(AbstractUser):
	CHOICES = (
		(1, 'administrativo'),
		(2, 'docente'),
		(3, 'padre'),
		(4, 'estudiante'),
		(5, 'administrador')
	)
	first_name = models.CharField(
		max_length=100,
		null=False,
		blank=False,
		validators=[
			RegexValidator(
				regex=r'^[a-zA-ZñÑáéíóúÁÉÍÓÚ]',
				message='El campo sólo permite letras',
				code='Numero Invalido'
				)
			]
		)
	email = models.CharField(
		max_length=70,
		null=False,
		blank=False,
		validators=[
			RegexValidator(
				regex=r'^[^@]+@[^@]+\.[a-zA-Z]{2,}$',
				message='No es un correo válido',
				code='Numero Invalido'
				)
			]
		)
	tipo_usuario = models.PositiveSmallIntegerField(choices=CHOICES, default=5)

class Administrativo(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True, related_name='administrativo')
	ci = models.CharField(
		max_length=9,
		null=False,
		blank=False,
		unique=True,
		validators=[
			RegexValidator(
				regex=r'[0-9]{7}[a-zA-Z]{0,2}',
				message='El CI Tiene un máximo de 7 digitos y en algunos casos dos letras mas',
				code='Numero Invalido'
				)
			]
		)
	telefono_celular = models.CharField(
		max_length = 8,
		null=False,
		blank=False,
		unique=True,
		validators=[
			RegexValidator(
				regex=r'^[0-9]{8}$',
				message='Teléfono celular (Solo 8 digitos)',
				code='Numero Invalido'
				)
			]
		)
	telefono_fijo = models.CharField(
		max_length = 7,
		blank=True,
		validators=[
			RegexValidator(
				regex=r'^[0-9]{7}',
				message='Teléfono fijo (Solo 7 digitos)',
				code='Numero Invalido'
				)
			]
		)
	profesion = models.CharField(
		max_length=50,
		null=False,
		blank=False,
		validators=[
			RegexValidator(
				regex=r'^[a-zA-ZñÑáéíóúÁÉÍÓÚ]{3,}$',
				message='El campo debe contener solo letras',
				code='Numero Invalido'
				)
			]
		)
	puesto = models.CharField(
		max_length=50,
		null=False,
		blank=False,
		validators=[
			RegexValidator(
				regex=r'^[a-zA-ZñÑáéíóúÁÉÍÓÚ]{3,}$',
				message='El campo debe contener solo letras',
				code='Numero Invalido'
				)
			]
		)
	fecha_ingreso = models.DateField(
		null=False,
		blank=False
		)
	domicilio = models.CharField(
		max_length=30,
		null=False,
		blank=False
		)

	def __str__(self):
		return str(self.user)

	def nombre_usuario(self):
		nombres = self.user.first_name
		apellidos = self.user.last_name
		ci = self.ci
		aux = nombres[0].lower()
		aux1 = apellidos.split(" ")
		aux2 = aux1[0].lower()
		user = aux + aux2 + ci
		return user

	def pass_usuario(self):
		nombres = self.user.first_name
		apellidos = self.user.last_name
		ci = self.ci
		aux = nombres[0].lower()
		aux1 = apellidos.split(" ")
		aux2 = aux1[0].lower()
		passw = aux + aux2 + ci
		return passw

	def save(self, *args, **kwargs):
		super(Administrativo, self).save(*args, **kwargs)
		self.user.tipo_usuario = 1
		self.user.username = self.nombre_usuario()
		self.user.set_password(self.pass_usuario())
		self.user.save()

class Docente(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True, related_name='docente')
	ci = models.CharField(
		max_length=9,
		null=False,
		blank=False,
		unique=True,
		validators=[
			RegexValidator(
				regex=r'[0-9]{7}[a-zA-Z]{0,2}',
				message='El CI Tiene un máximo de 7 digitos y en algunos casos dos letras mas',
				code='Numero Invalido'
				)
			]
		)
	telefono_celular = models.CharField(
		max_length = 8,
		null=False,
		blank=False,
		unique=True,
		validators=[
			RegexValidator(
				regex=r'^[0-9]{8}$',
				message='Teléfono celular (Solo 8 digitos)',
				code='Numero Invalido'
				)
			]
		)
	telefono_fijo = models.CharField(
		max_length = 7,
		blank=True,
		validators=[
			RegexValidator(
				regex=r'^[0-9]{7}',
				message='Teléfono fijo (Solo 7 digitos)',
				code='Numero Invalido'
				)
			]
		)
	curso = models.ManyToManyField('educativo.Curso', help_text=mark_safe('<ul><li>Seleccione los cursos en los que dicta clases el/la docente.</li><li>Puede seleccionar un solo elemento haciendo click en él.</li><li>Para seleccionar varios elementos, mantenga presionada la tecla "ctrl" y seleccione los elementos.</li></ul>'))
	materia = models.ManyToManyField('educativo.Materia', help_text=mark_safe('<ul><li>Seleccione las materias que dicta el/la docente.</li><li>Puede seleccionar un solo elemento haciendo click en él.</li><li>Para seleccionar varios elementos, mantenga presionada la tecla "ctrl" y seleccione los elementos.</li></ul>'))
	fecha_ingreso = models.DateField(
		null=False,
		blank=False
		)
	domicilio = models.CharField(
		max_length=30,
		null=False,
		blank=False
		)

	def __str__(self):
		return self.user.first_name + " " + self.user.last_name
	
	def fecha_f(self):
		return self.fecha_ingreso.strftime("%d/%m/%y")

	def nombre_usuario(self):
		nombres = self.user.first_name
		apellidos = self.user.last_name
		ci = self.ci
		aux = nombres[0].lower()
		aux1 = apellidos.split(" ")
		aux2 = aux1[0].lower()
		user = aux + aux2 + ci
		return user

	def pass_usuario(self):
		nombres = self.user.first_name
		apellidos = self.user.last_name
		ci = self.ci
		aux = nombres[0].lower()
		aux1 = apellidos.split(" ")
		aux2 = aux1[0].lower()
		passw = aux + aux2 + ci
		return passw

	def save(self, *args, **kwargs):
		super(Docente, self).save(*args, **kwargs)
		self.user.tipo_usuario = 2
		self.user.username = self.nombre_usuario()
		self.user.set_password(self.pass_usuario())
		self.user.save()

class Padre(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True, related_name='padre')
	ci = models.CharField(
		max_length=9,
		null=False,
		blank=False,
		unique=True,
		validators=[
			RegexValidator(
				regex=r'[0-9]{7}[a-zA-Z]{0,2}',
				message='El CI Tiene un máximo de 7 digitos y en algunos casos dos letras mas',
				code='Numero Invalido'
				)
			]
		)
	telefono_celular = models.CharField(
		max_length = 8,
		null=False,
		blank=False,
		unique=True,
		validators=[
			RegexValidator(
				regex=r'^[0-9]{8}$',
				message='Teléfono celular (Solo 8 digitos)',
				code='Numero Invalido'
				)
			]
		)
	telefono_fijo = models.CharField(
		max_length = 7,
		blank=True,
		validators=[
			RegexValidator(
				regex=r'^[0-9]{7}',
				message='Teléfono fijo (Solo 7 digitos)',
				code='Numero Invalido'
				)
			]
		)
	parentezco = models.CharField(
		max_length=2,
		null=False,
		blank=False,
		choices=(('1', 'Padre/Madre de familia'),('2','Abuelo/a'),('3', 'Tío/a'),('4','Otro')),
		help_text="Grado de parentezco con los alumnos inscritos por el mismo."
		)
	ocupacion = models.CharField(
		max_length=50,
		blank=True
		)
	lugar_trabajo = models.CharField(
		max_length=60,
		blank=True,
		validators=[
			RegexValidator(
				regex=r'^[a-zA-ZñÑáéíóúÁÉÍÓÚ0-9]{5,}$',
				message='El campo debe contener solo letras y números',
				code='Numero Invalido'
				)
			]
		)
	domicilio = models.CharField(
		max_length=30,
		null=False,
		blank=False
		)
	apoderado = models.BooleanField(
		default=False,
		help_text='Marque esta opción en caso de que el familiar sea apoderado del estudiante'
		)

	def __str__(self):
		return self.user.first_name + " " + self.user.last_name

	def nombre_usuario(self):
		nombres = self.user.first_name
		apellidos = self.user.last_name
		ci = self.ci
		aux = nombres[0].lower()
		aux1 = apellidos.split(" ")
		aux2 = aux1[0].lower()
		user = aux + aux2 + ci
		return user

	def pass_usuario(self):
		nombres = self.user.first_name
		apellidos = self.user.last_name
		ci = self.ci
		aux = nombres[0].lower()
		aux1 = apellidos.split(" ")
		aux2 = aux1[0].lower()
		passw = aux + aux2 + ci
		return passw

	def save(self, *args, **kwargs):
		super(Padre, self).save(*args, **kwargs)
		self.user.tipo_usuario = 3
		self.user.username = self.nombre_usuario()
		self.user.set_password(self.pass_usuario())
		self.user.save()

class Estudiante(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True, related_name='estudiante')
	ci = models.CharField(
		max_length=9,
		blank=True,
		validators=[
			RegexValidator(
				regex=r'[0-9]{7}[a-zA-Z]{0,2}',
				message='El CI Tiene un máximo de 7 digitos y en algunos casos dos letras mas',
				code='Numero Invalido'
				)
			]
		)
	rude = models.CharField(
		max_length=16,
		null=False,
		blank=False,
		unique=True,
		validators=[
			RegexValidator(
				regex=r'[0-9]{14,16}[a-zA-Z]{0,1}',
				message='RUDE tiene un máximo de 16 dígitos, debe contener sólo números y en algunos casos una letra más.',
				code='Numero Invalido'
				)
			]
		)
	telefono_celular = models.CharField(
		max_length = 8,
		blank=True,
		validators=[
			RegexValidator(
				regex=r'^[0-9]{8}$',
				message='Teléfono celular (Solo 8 digitos)',
				code='Numero Invalido'
				)
			]
		)
	padre = models.ForeignKey(Padre, on_delete=models.CASCADE)
	curso = models.ForeignKey('educativo.Curso', on_delete=models.CASCADE, help_text="Escoja el curso al que pertenece el estudiante")
	sexo = models.CharField(
		max_length=2,
		null=False,
		blank=False,
		choices=(('M', 'Masculino'),('F', 'Femenino'))
		)
	observaciones = models.TextField(
		blank=True,
		help_text="Aquí agregue algunos aspectos a considerar del alumno Ej: Condición médica."
		)

	def __str__(self):
		return self.user.first_name + " " + self.user.last_name

	def nombre_usuario(self):
		return self.rude

	def pass_usuario(self):
		nombres = self.user.first_name
		apellidos = self.user.last_name
		rude = self.rude
		aux = nombres[0].lower()
		aux1 = apellidos.split(" ")
		aux2 = aux1[0].lower()
		passw = aux + aux2 + rude
		return passw

	def save(self, *args, **kwargs):
		super(Estudiante, self).save(*args, **kwargs)
		self.user.tipo_usuario = 4
		self.user.username = self.nombre_usuario()
		self.user.set_password(self.pass_usuario())
		self.user.save()