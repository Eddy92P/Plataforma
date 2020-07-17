from django.forms import ModelForm
from django import forms
from apps.comunidad.models import *
from django.contrib.auth import get_user_model

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from django.core.validators import RegexValidator

from django.urls import reverse

class Html5DateInput(forms.DateInput):
	input_type = 'date'

class crearUsuarioUserAForm(UserCreationForm):
	class Meta:
		User = get_user_model()
		model = User
		fields =[
			'first_name',
			'last_name',
			'email'
		]
		labels = {
			'first_name' : 'Nombres'
		}
		widgets ={
			'username':forms.TextInput(attrs={'class': 'form-control'}),
			'first_name':forms.TextInput(attrs={'class': 'form-control'}),
			'last_name':forms.TextInput(attrs={'class': 'form-control'}),
			'email':forms.EmailInput(attrs={'class': 'form-control'}),
		}
	def __init__(self, *args, **kwargs):
		super(crearUsuarioUserAForm, self).__init__(*args, **kwargs)
		self.fields['email'].required = True
		self.fields['first_name'].required = True
		self.fields['last_name'].required = True
		self.fields['password1'].required = False
		self.fields['password2'].required = False
		self.fields['password1'].widget = forms.HiddenInput()
		self.fields['password2'].widget = forms.HiddenInput()

class crearKardexAdministrativoForm(ModelForm):
	class Meta:
		model = Administrativo
		exclude = ['user']
		widgets ={
			'fecha_ingreso':Html5DateInput(format='%Y-%m-%d', attrs={'class':'form-control'}),
			'ci':forms.TextInput(attrs={'class':'form-control'}),
			'telefono_celular':forms.TextInput(attrs={'class':'form-control'}),
			'telefono_fijo':forms.TextInput(attrs={'class':'form-control'}),
			'domicilio':forms.TextInput(attrs={'class':'form-control'}),
			'profesion':forms.TextInput(attrs={'class':'form-control'}),
		}
		labels = {
			'ci':'C.I.',
			'telefono_fijo':'Teléfono fijo',
			'telefono_celular':'Teléfono celular',
			'profesion':'Profesión',
			'fecha_ingreso':'Fecha de ingreso',
			'puesto':'Puesto de trabajo'
		}

class crearUsuarioUserBForm(UserCreationForm):
	class Meta:
		User = get_user_model()
		model = User
		fields =[
			'first_name',
			'last_name',
			'email',
		]
		labels = {
			'first_name' : 'Nombres'
		}
		widgets ={
			'username':forms.TextInput(attrs={'class': 'form-control'}),
			'first_name':forms.TextInput(attrs={'class': 'form-control'}),
			'last_name':forms.TextInput(attrs={'class': 'form-control'}),
			'email':forms.EmailInput(attrs={'class': 'form-control'}),
		}

	def __init__(self, *args, **kwargs):
		super(crearUsuarioUserBForm, self).__init__(*args, **kwargs)
		self.fields['email'].required = True
		self.fields['first_name'].required = True
		self.fields['last_name'].required = True
		self.fields['password1'].required = False
		self.fields['password2'].required = False
		self.fields['password1'].widget = forms.HiddenInput()
		self.fields['password2'].widget = forms.HiddenInput()

class crearKardexDocenteForm(ModelForm):
	class Meta:
		model = Docente
		exclude = ['user']
		widgets ={
			'fecha_ingreso':Html5DateInput(format='%Y-%m-%d', attrs={'class':'form-control'}),
			'ci':forms.TextInput(attrs={'class':'form-control'}),
			'telefono_celular':forms.TextInput(attrs={'class':'form-control'}),
			'telefono_fijo':forms.TextInput(attrs={'class':'form-control'}),
			'domicilio':forms.TextInput(attrs={'class':'form-control'}),
			'profesion':forms.TextInput(attrs={'class':'form-control'}),
		}
		labels = {
			'ci':'C.I.',
			'telefono_fijo':'Teléfono fijo',
			'telefono_celular':'Teléfono celular',
			'profesion':'Profesión',
			'fecha_ingreso':'Fecha de ingreso',
			'materia':'Materias',
			'curso':'Curso/s'
		}

class crearUsuarioUserCForm(UserCreationForm):
	class Meta:
		User = get_user_model()
		model = User
		fields =[
			'first_name',
			'last_name',
			'email',
			'is_active'
		]
		labels = {
			'first_name' : 'Nombres'
		}
		widgets ={
			'username':forms.TextInput(attrs={'class': 'form-control'}),
			'first_name':forms.TextInput(attrs={'class': 'form-control'}),
			'last_name':forms.TextInput(attrs={'class': 'form-control'}),
			'email':forms.EmailInput(attrs={'class': 'form-control'}),
		}

	def __init__(self, *args, **kwargs):
		super(crearUsuarioUserCForm, self).__init__(*args, **kwargs)
		self.fields['email'].required = True
		self.fields['first_name'].required = True
		self.fields['last_name'].required = True
		self.fields['password1'].required = False
		self.fields['password2'].required = False
		self.fields['password1'].widget = forms.HiddenInput()
		self.fields['password2'].widget = forms.HiddenInput()

class crearKardexPadreForm(ModelForm):
	class Meta:
		model = Padre
		exclude = ['user']
		widgets ={
			'ci':forms.TextInput(attrs={'class':'form-control'}),
			'telefono_celular':forms.TextInput(attrs={'class':'form-control'}),
			'telefono_fijo':forms.TextInput(attrs={'class':'form-control'}),
		}
		labels = {
			'ci':'C.I.',
			'telefono_fijo':'Teléfono fijo',
			'telefono_celular':'Teléfono celular',
			'domicilio':'Dirección',
			'lugar_trabajo':'Lugar de trabajo'
		}

class crearUsuarioUserDForm(UserCreationForm):
	class Meta:
		User = get_user_model()
		model = User
		fields =[
			'first_name',
			'last_name',
			'email',
			'is_active'
		]
		labels = {
			'first_name' : 'Nombres'
		}
		widgets ={
			'username':forms.TextInput(attrs={'class': 'form-control'}),
			'first_name':forms.TextInput(attrs={'class': 'form-control'}),
			'last_name':forms.TextInput(attrs={'class': 'form-control'}),
			'email':forms.EmailInput(attrs={'class': 'form-control'}),
		}
		
	def __init__(self, *args, **kwargs):
		super(crearUsuarioUserDForm, self).__init__(*args, **kwargs)
		self.fields['email'].required = False
		self.fields['first_name'].required = True
		self.fields['last_name'].required = True
		self.fields['password1'].required = False
		self.fields['password2'].required = False
		self.fields['password1'].widget = forms.HiddenInput()
		self.fields['password2'].widget = forms.HiddenInput()

class crearKardexEstudianteForm(ModelForm):
	class Meta:
		model = Estudiante
		exclude = ['user']
		widgets ={
			'ci':forms.TextInput(attrs={'class':'form-control'}),
			'telefono_celular':forms.TextInput(attrs={'class':'form-control'}),
		}
		labels = {
			'ci':'C.I.',
			'rude':'RUDE',
			'telefono_celular':'Teléfono celular',
			'direccion':'Dirección',
			'padre':'Padre o tutor'
		}

CHOICES = (('1','ID'),('2','Nombre'),)
class searchForm(forms.Form):
	search = forms.IntegerField(label="", help_text="", widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Busqueda por...'}))
	buscar_por = forms.ChoiceField(label="", help_text="", choices=CHOICES)

class addPermissionsForm(forms.Form):
	mod_personal = forms.BooleanField(label="Otorgar permiso para el modulo usuarios", required=False)
	mod_contabilidad = forms.BooleanField(label="Otorgar permiso para el modulo contabilidad", required=False)
	mod_cargas = forms.BooleanField(label="Otorgar permiso para el modulo cargas", required=False)

class updateUsuarioUserForm(ModelForm):
	#email = forms.EmailField(required=True)
	class Meta:
		model=User
		fields=[
			#'username',
			'first_name',
			'last_name',
			'email',
		]
		widgets = {
			#'username':forms.TextInput(attrs={'class':'form-control'}),
			'first_name':forms.TextInput(attrs={'class':'form-control'}),
			'last_name':forms.TextInput(attrs={'class':'form-control'}),
			'email':forms.EmailInput(attrs={'class':'form-control'}),
		}
	def __init__(self, *args, **kwargs):
		super(updateUsuarioUserForm, self).__init__(*args, **kwargs)
		self.fields['email'].required = True
		self.fields['first_name'].required = True
		self.fields['last_name'].required = True

class crearModificarKardexAdminForm(ModelForm):
	class Meta:
		model = Administrativo
		fields = [		
			'telefono_fijo',
			'telefono_celular',
			'domicilio',
		]
		widgets = {
			'telefono_fijo':forms.TextInput(attrs={'class':'form-control'}),
			'telefono_celular':forms.TextInput(attrs={'class':'form-control'}),
			'domicilio':forms.TextInput(attrs={'class':'form-control'}),
		}

class crearModificarKardexDocenteForm(ModelForm):
	class Meta:
		model = Docente
		fields = [		
			'telefono_fijo',
			'telefono_celular',
			'domicilio',
		]
		widgets = {
			'telefono_fijo':forms.TextInput(attrs={'class':'form-control'}),
			'telefono_celular':forms.TextInput(attrs={'class':'form-control'}),
			'domicilio':forms.TextInput(attrs={'class':'form-control'}),
		}

class crearModificarKardexPadreForm(ModelForm):
	class Meta:
		model = Padre
		fields = [		
			'telefono_fijo',
			'telefono_celular',
			'domicilio',
		]
		widgets = {
			'telefono_fijo':forms.TextInput(attrs={'class':'form-control'}),
			'telefono_celular':forms.TextInput(attrs={'class':'form-control'}),
			'domicilio':forms.TextInput(attrs={'class':'form-control'}),
		}

class crearModificarKardexEstudianteForm(ModelForm):
	class Meta:
		model = Estudiante
		fields = [		
			'telefono_celular',
		]
		widgets = {
			'telefono_celular':forms.TextInput(attrs={'class':'form-control'}),
		}

class darBajaForm(ModelForm):
	class Meta:
		model = User
		fields = [
			'is_active'
		]
