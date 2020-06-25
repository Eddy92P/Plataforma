from django.forms import ModelForm
from django import forms
from apps.educativo.models import *

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User

from django.urls import reverse

from dal import autocomplete

class Html5DateInput(forms.DateInput):
	input_type = 'date'

class Html5DateTimeInput(forms.DateTimeInput):
	input_type = 'datetime-local'

	def __init__(self, **kwargs):
		kwargs["format"] = "%Y-%m-%dT%H:%M"
		super().__init__(**kwargs)

class crearCursoForm(ModelForm):
	class Meta:
		model = Curso
		exclude = ['']

class crearMateriaForm(ModelForm):
	class Meta:
		model = Materia
		exclude = ['actualizacion']
		labels = {
			'curso': 'Cursos',
		}

class crearActividadForm(ModelForm):
	class Meta:
		model = Actividad
		exclude = ['']
		widgets = {'fecha_inicio':Html5DateInput(format='%Y-%m-%d', attrs={'class':'form-control'}), 'fecha_fin':Html5DateInput(format='%Y-%m-%d', attrs={'class':'form-control'})}
		labels = {
			'ubicacion' : 'Ubicación',
			'descripcion' : 'Descripción'
		}

class crearTemaForm(ModelForm):
	class Meta:
		model = Tema
		exclude = ['curso']
		labels = {
			'nombre': 'Título del tema',
			'contenido': 'Contenido del tema'
		}

class crearTareaEstudianteForm(ModelForm):
	class Meta:
		model = Tarea_estudiante
		exclude = ['estudiante', 'tarea', 'entregado', 'fecha_entrega']

class crearTareaForm(ModelForm):
	class Meta:
		model = Tarea
		exclude = ['fecha_habilitado', 'docente', 'tema']
		widgets = {
			'fecha_plazo':Html5DateTimeInput(attrs={'class':'form-control'}),
		}
		labels = {
			'estudiante' : 'Estudiantes',
			'nombre': 'Nombre de la tarea',
			'seleccionar': 'Seleccionar todo',
			'trabajo' : 'Guía para realizar el trabajo'
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["fecha_plazo"].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]

class crearMaterialForm(ModelForm):
	class Meta:
		model = Material
		exclude = ['docente', 'fecha', 'subido', 'tema']
		labels = {
			'descripcion': 'Descripción del material',
			'trabajo' : 'Material'
		}

class crearObservacionForm(ModelForm):
	class Meta:
		model = Observacion
		exclude = ['docente', 'fecha']
		widgets = {
			'curso':autocomplete.ModelSelect2(url='educativo:curso_autocomplete'),
			'materia':autocomplete.ModelSelect2(url='educativo:materia_autocomplete', forward=['curso']),
			'estudiante':autocomplete.ModelSelect2(url='educativo:estudiante_autocomplete', forward=['curso']),
		}
		labels = {
			'razon': 'Motivo',
			'descripcion' : 'Descripción'
		}

class crearComentarioForm(ModelForm):
	class Meta:
		model = Comentario
		exclude = ['usuario', 'fecha']
		labels = {
			'razon' : 'Motivo',
			'descripcion' : 'Descripción'
		}

class crearPensionForm(ModelForm):
	class Meta:
		model = Pension
		exclude = ['administrativo']
		labels = {
			'estado': 'Pendiente',
			'numero_pension' : 'Número de pensión'
		}
		widgets = {
			'estudiante':autocomplete.ModelSelect2(url='educativo:estudiante_autocomplete'),
		}

class searchForm(forms.Form):
	docente = forms.CharField(required=False, label="Profesor", widget=forms.TextInput(attrs={"placeholder": "Escriba el nombre o apellido", 'class':'form-control mb-2 col-md-11'}))
	fecha1 = forms.CharField(label="Fecha inicial", help_text="", widget=Html5DateInput(format='%Y-%m-%d', attrs={'class':'form-control mb-2 col-md-9'}))
	fecha2 = forms.CharField(label="Fecha final", help_text="", widget=Html5DateInput(format='%Y-%m-%d', attrs={'class':'form-control mb-2 col-md-9'}))
