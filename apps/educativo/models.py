# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib.auth.models import User
from apps.comunidad import apps

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from django.db import models
from apps.comunidad.models import Docente, Estudiante

import os
import datetime

def validate_file_extension(value):
	ext = os.path.splitext(value.name)[1]
	valid_extensions = ['.pdf','.doc','.docx', '.png', '.gif', '.jpg']
	if not ext in valid_extensions:
		raise ValidationError(u'Tipo de archivo no soportado')

def validate_image_extension(value):
	ext = os.path.splitext(value.name)[1]
	valid_extensions = ['.jpg','.gif','.png']
	if not ext in valid_extensions:
		raise ValidationError(u'Tipo de archivo no soportado')

def validate_file_size_e(value):
	file_size = value.file.size
	limit_kb = 3000
	if file_size > limit_kb*1024:
		raise ValidationError(u"El tamaño máximo permitido es de 3MB")

def validate_file_size_d(value):
	file_size = value.file.size
	limit_kb = 3000
	if file_size > limit_kb*1024:
		raise ValidationError(u"El tamaño máximo permitido es de 3MB")

def validate_file_size_d_m(value):
	file_size = value.file.size
	limit_kb = 7000
	if file_size > limit_kb*1024:
		raise ValidationError(u"El tamaño máximo permitido es de 7MB")

class Curso(models.Model):
	ciclo = models.CharField(
		max_length=1,
		null=False,
		blank=False,
		help_text="Escoja el ciclo al que pertenece este curso.",
		choices=(('I', 'Inicial'), ('P', 'Primaria'), ('S', 'Secundaria'))
		)
	nombre = models.CharField(
		max_length=35,
		null=False,
		blank=False,
		help_text="Ej: Primero, Segundo, Tercero, etc."
		)
		
	def __str__(self):
		return self.nombre

	def docente_enc(self):
		return Docente.objects.filter(curso__id=self.id)

class Materia_curso(models.Model):
	materia = models.ForeignKey('Materia', on_delete=models.PROTECT)
	curso = models.ForeignKey(Curso, on_delete=models.PROTECT)

class Materia(models.Model):
	nombre = models.CharField(
		unique=True,
		max_length = 30,
		null=False,
		blank=False,
		help_text="Ingrese el nombre de la materia, como por ejemplo, matemáticas, literatura.",
		validators=[
			RegexValidator(
				regex=r'^[a-zA-ZñÑáéíóúÁÉÍÓÚ]{5,}',
				message='El campo sólo permite letras y un mínimo de 5 caracteres',
				code='Numero Invalido'
				)
			]
		)
	curso = models.ManyToManyField(Curso, help_text='<ul><li>Seleccione los cursos en los que se dictan esta materia.</li><li>Seleccione solo un elemento haciendo click en él.<li>Para seleccionar varios elementos mantenga presionada la tecla "ctrl" y seleccione dichos elementos.</li></ul>', through='Materia_curso')
	actualizacion = models.DateTimeField(
		auto_now = True,
		null=False,
		blank=False
		)
	
	imagen = models.ImageField(
		null=False,
		blank=False,
		upload_to='imagenes_materias/',
		validators=[validate_image_extension, validate_file_size_d],
		help_text="<ul><li>Escoja una imagen que identifique la materia.</li><li>Los fomatos permitidos son .jpg, .gif y .png</li></ul>"
		)

	def __str__(self):
		return self.nombre

	def docente_enc(self):
		return Docente.objects.filter(materia__in=Materia.objects.filter(id=self.id))

	def docente_encargado(self, curso_id):
		qs1 = Docente.objects.filter(materia__in=Materia.objects.filter(id=self.id))
		qs2 = Docente.objects.filter(curso__in=Curso.objects.filter(id=curso_id))
		return qs1 & qs2

	def actualizacion_materia(self):
		diferencia_fechas = datetime.datetime.now() - self.actualizacion
		duration_in_s = diferencia_fechas.total_seconds()
		days = divmod(duration_in_s, 86400)
		hours = divmod(days[1], 3600)
		minutes = divmod(hours[1], 60)
		seconds = divmod(minutes[1], 1)
		if (days[0] > 1 )| (days[0] == 0):
			days_str = " dias "
		else:
			days_str = " día "
		if (hours[0] > 1) | (hours[0] == 0):
			hours_str = " horas "
		else:
			hours_str = " hora "
		if (minutes[0] > 1) | (minutes[0] == 1):
			minutes_str = " minutos y "
		else:
			minutes_str = " minuto y "
		if (seconds[0] > 1) | (seconds[0] == 0):
			seconds_str = " segundos. "
		else:
			seconds_str = " segundo. "
		return str(int(days[0])) + days_str + str(int(hours[0])) + hours_str + str(int(minutes[0])) + minutes_str + str(int(seconds[0])) + seconds_str

	def temas(self, curso, f1, f2):
		return Tema.objects.filter(materia=self.id, curso=curso , fecha_inicio__range=(f1, f2))

class Actividad(models.Model):
	nombre = models.CharField(
		max_length = 50,
		null=False,
		blank=False,
		help_text="Nombre de la actividad",
		validators=[
			RegexValidator(
				regex=r'^[a-zA-ZñÑáéíóúÁÉÍÓÚ]',
				message='El campo sólo permite letras',
				code='Numero Invalido'
				)
			]
		)
	ubicacion = models.CharField(
		max_length = 40,
		null=False,
		blank=False,
		help_text="Dónde se llevará acabo la actividad",
		validators=[
			RegexValidator(
				regex=r'^[a-zA-ZñÑáéíóúÁÉÍÓÚ]',
				message='El campo sólo permite letras',
				code='Numero Invalido'
				)
			]
		)
	descripcion = models.TextField(
		null=False,
		blank=False,
		help_text="Descripción de la actividad",
		)
	fecha_inicio = models.DateField(
		null=False,
		blank=False,
		help_text="Fecha en que iniciara la actividad."
		)
	fecha_fin = models.DateField(
		null=False,
		blank=False,
		help_text="Fecha en que finalizará la actividad."
		)

	class Meta:
		verbose_name_plural = "Actividades"

	def __str__(self):
		return self.nombre

class Tema(models.Model):
	curso = models.ForeignKey(Curso, on_delete=models.CASCADE, help_text="Seleccione el curso.")
	materia = models.ForeignKey(Materia, on_delete=models.CASCADE, help_text="Seleccione la materia.")
	num_tema = models.PositiveSmallIntegerField(
		null=False
		)
	fecha_inicio = models.DateField(
		auto_now_add = True,
		null=False,
		blank=False
		) 
	nombre = models.CharField(
		max_length=100,
		null=False,
		blank=False
		)
	contenido = models.TextField(
		null=False,
		blank=False
		)

	def __str__(self):
		return self.nombre

	def tareas(self, f1, f2):
		return Tarea.objects.filter(tema=self.id, fecha_habilitado__range=(f1, f2))

class Tarea_estudiante(models.Model):
	estudiante = models.ForeignKey('comunidad.Estudiante', on_delete=models.PROTECT)
	tarea = models.ForeignKey('Tarea', on_delete=models.PROTECT)
	trabajo = models.FileField(
		null=False,
		blank=False,
		upload_to='tareas_estudiantes/',
		validators=[validate_file_extension, validate_file_size_e],
		help_text = "Los fomatos permitidos son .pdf, .doc, .docx, .jpg, .gif, .jpg y debe tener un tamaño máximo de 3MB"
		)
	fecha_entrega = models.DateTimeField(
		auto_now_add = False,
		null = True,
		blank = True
		)
	entregado = models.BooleanField(default=False)
	revisado = models.BooleanField(default=False, help_text='Marque esta opción para indicar que se revisó la tarea.')
	observaciones = models.TextField(
		null=False,
		blank=False
		)

	def lapso_retraso(self):
		diferencia_fechas = datetime.datetime.now() - self.tarea.fecha_plazo
		duration_in_s = diferencia_fechas.total_seconds()
		days = divmod(duration_in_s, 86400)
		hours = divmod(days[1], 3600)
		minutes = divmod(hours[1], 60)
		seconds = divmod(minutes[1], 1)
		if (days[0] > 1 )| (days[0] == 0):
			days_str = " dias "
		else:
			days_str = " día "
		if (hours[0] > 1) | (hours[0] == 0):
			hours_str = " horas "
		else:
			hours_str = " hora "
		if (minutes[0] > 1) | (minutes[0] == 1):
			minutes_str = " minutos y "
		else:
			minutes_str = " minuto y "
		if (seconds[0] > 1) | (seconds[0] == 0):
			seconds_str = " segundos. "
		else:
			seconds_str = " segundo. "
		return str(int(days[0])) + days_str + str(int(hours[0])) + hours_str + str(int(minutes[0])) + minutes_str + str(int(seconds[0])) + seconds_str

	def filename(self):
		return os.path.basename(self.trabajo.name)

	def fecha_entrega_corta(self):
		return self.fecha_entrega.strftime("%d-%m-%y a las %H:%M")

class Tarea(models.Model):
	tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
	num_tarea = models.PositiveSmallIntegerField(
		null = False
		)
	estudiante = models.ManyToManyField('comunidad.Estudiante', through='Tarea_estudiante', help_text='<ul><li>ADVERTENCIA!!! si selecciona un elemento de la lista ya no podrá seleccionar todos los estudiantes con el botón "Seleccionar todo", en caso de hacerlo, recargue la página para poder seleccionar a todos los estudiantes.</li><li>Seleccione los alumnos a los que se enviará la tarea.</li><li>O puede marcar la opción "Seleccionar todo", para seleccionar a todos los alumnos.</li></ul>')
	seleccionar = models.BooleanField(
		default=False
		)
	docente = models.ForeignKey('comunidad.Docente', on_delete=models.CASCADE)
	nombre = models.CharField(
		max_length=100,
		null=False,
		blank=False
		)
	fecha_plazo = models.DateTimeField(
		null=False,
		blank = False,
		help_text = 'Debe seleccionar la fecha y hora máximos, para la entrega de tareas.'
		)
	fecha_habilitado = models.DateField(
		auto_now_add=True
		)
	trabajo = models.FileField(
		null=False,
		blank=False,
		upload_to='tareas_docentes/',
		validators=[validate_file_extension, validate_file_size_d],
		help_text = "Los fomatos permitidos son .pdf, .doc, .docx, .png, .jpg, .gif y debe tener un tamaño máximo de 3MB"
		)

	def __str__(self):
		return self.nombre

	def filename(self):
		return os.path.basename(self.trabajo.name)

class Material(models.Model):
	docente = models.ForeignKey('comunidad.Docente', on_delete=models.CASCADE)
	tema = models.ForeignKey(Tema, on_delete=models.CASCADE)
	descripcion = models.CharField(
		max_length=60,
		null=False,
		blank=False
		)
	trabajo = models.FileField(
		null=False,
		blank=False,
		upload_to='material_docentes/',
		validators=[validate_file_extension, validate_file_size_d_m],
		help_text = "Los fomatos permitidos son .pdf, .doc, .docx y debe tener un tamaño máximo de 7MB"
		)
	fecha = models.DateField(
		auto_now_add=True,
		null=False,
		blank=False
		)

	def filename(self):
		return os.path.basename(self.trabajo.name)

	class Meta:
		verbose_name_plural = "Materiales"

class Observacion(models.Model):
	docente = models.ForeignKey('comunidad.Docente', on_delete=models.CASCADE)
	curso = models.ForeignKey(Curso, on_delete=models.CASCADE, help_text='<ul><li>PARA EMPEZAR CON EL LLENADO DEL FORMULARIO DEBE SELECCIONAR PRIMERO UN ELEMENTO DE ESTA LISTA.</li><li>Seleccione el curso al que pertenece el estudiante.</li><li>Puede buscar un curso específico escribiendo el nombre en el cuadro de texto.</li></ul>')
	materia = models.ForeignKey(Materia, on_delete=models.CASCADE, help_text='<ul><li>Seleccione la materia.</li><li>Puede buscar una materia específica escribiendo el nombre en el cuadro de texto.</li><li>En caso de no existir una materia que pertenezca al curso seleccionado este cuadro se mostrará como "No se encontraron resultados".</li></ul>')
	estudiante = models.ForeignKey('comunidad.Estudiante', on_delete=models.CASCADE, help_text='<ul><li>Seleccione el estudiante.</li><li>Puede buscar un/una estudiante específic@ escribiendo su nombre en el cuadro de texto.</li><li>En caso de no existir un/una estudiante que pertenezca al curso seleccionado este cuadro se mostrará como "No se encontraron resultados."</li></ul>')
	fecha = models.DateField(
		auto_now_add=True,
		null=False,
		blank=False
		)
	razon = models.CharField(
		max_length=2,
		null=False,
		blank=False,
		choices=(('1', 'Indisciplina'), ('2', 'Tareas'), ('3', 'Felicitaciones')),
		help_text='Motivo por el cual se realiza la observación.'
		)
	descripcion = models.TextField(
		null=False,
		blank=False
		)

	class Meta:
		verbose_name_plural = "Observaciones"

class Comentario(models.Model):
	usuario = models.ForeignKey('comunidad.User', on_delete=models.CASCADE)
	fecha = models.DateTimeField(
		auto_now_add=True,
		null=False,
		blank=False
		)
	razon = models.CharField(
		max_length=2,
		null=False,
		blank=False,
		choices=(('1', 'Opinión'), ('2', 'Queja'), ('3', 'Observación')),
		help_text='Motivo de su comentario.'
		)
	descripcion = models.TextField(
		null=False,
		blank=False
		)

class Pension(models.Model):
	estudiante = models.ForeignKey('comunidad.Estudiante', on_delete=models.CASCADE, help_text='Seleccione un estudiante, o escriba el nombre en el cuadro de texto para realizar la búsqueda.')
	administrativo = models.ForeignKey('comunidad.Administrativo', on_delete=models.CASCADE)
	numero_pension = models.PositiveSmallIntegerField(
		null=False,
		blank=False
		)
	estado = models.BooleanField(
		default=False,
		help_text="Marque esta opción si la pensión está pendiente de pago."
		)

	class Meta:
		verbose_name_plural = "Pensiones"