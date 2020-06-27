# -*- coding: utf-8 -*-
from django.shortcuts import render

from django.views.generic.edit import FormMixin
from django.http import Http404
from django.utils.translation import ugettext as _

from django.views.generic import ListView, CreateView, UpdateView, FormView, DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from apps.comunidad.forms import *
from apps.comunidad.models import *
from apps.educativo.models import Materia, Curso
from django.contrib.auth.models import User

from django.contrib.auth.mixins import PermissionRequiredMixin

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from django.contrib.auth import get_user_model 

def main_page(request):
	return render(request,'base/index.html',{})

class crearUsuarioAdministrativo(CreateView):
	form_class = crearUsuarioUserAForm
	second_form_class = crearKardexAdministrativoForm
	template_name = 'comunidad/nuevousuarioadmin.html'
	success_url = reverse_lazy('comunidad:listausuarioadmin')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if 'form' not in context or 'form2' not in context:
			context['form'] = self.form_class()
			context['form2'] = self.second_form_class()
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST)
		form2 = self.second_form_class(request.POST)
		if form.is_valid() and form2.is_valid():
			permission = Permission.objects.get(codename='view_administrativo')
			permission2 = Permission.objects.get(codename='view_educativo')
			form2save = form2.save(commit=False)
			form2save.user = form.save()
			form2save.save()
			form2save.user.user_permissions.add(permission)
			form2save.user.user_permissions.add(permission2)
			return HttpResponseRedirect(self.success_url)
		else:
			return self.render_to_response(self.get_context_data(form=form, form2=form2))

class crearUsuarioDocente(CreateView):
	model = Materia
	second_model = Curso
	form_class = crearUsuarioUserBForm
	second_form_class = crearKardexDocenteForm
	template_name = 'comunidad/nuevousuariodocente.html'
	success_url = reverse_lazy('comunidad:listausuariodocente')

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		if (not self.second_model.objects.all().exists()) & (not self.model.objects.all().exists()):
			context['error'] = "Debe crear cursos y materias primero, antes de registrar un nuevo docente."
		elif not self.second_model.objects.all().exists():
			context['error'] = "Debe crear cursos primero, antes de registrar un nuevo docente."
		elif not self.model.objects.all().exists():
			context['error'] = "Debe crear materias primero, antes de registrar un nuevo docente."
		if 'form' not in context or 'form2' not in context:
			context['form'] = self.form_class()
			context['form2'] = self.second_form_class()
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST)
		form2 = self.second_form_class(request.POST)
		if form.is_valid() and form2.is_valid():
			permission = Permission.objects.get(codename='view_docente')
			permission2 = Permission.objects.get(codename='view_educativo')
			form2save = form2.save(commit=False)
			form2save.user = form.save()
			form2save.save()
			form2.save_m2m()
			form2save.user.user_permissions.add(permission2)
			form2save.user.user_permissions.add(permission)
			return HttpResponseRedirect(self.success_url)
		else:
			return self.render_to_response(self.get_context_data(form=form, form2=form2))

class crearUsuarioPadre(CreateView):
	form_class = crearUsuarioUserCForm
	second_form_class = crearKardexPadreForm
	template_name = 'comunidad/nuevousuariopadre.html'
	success_url = reverse_lazy('comunidad:listausuariopadre')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if 'form' not in context or 'form2' not in context:
			context['form'] = self.form_class()
			context['form2'] = self.second_form_class()
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST)
		form2 = self.second_form_class(request.POST)
		if form.is_valid() and form2.is_valid():
			permission = Permission.objects.get(codename='view_padre')
			permission2 = Permission.objects.get(codename='view_educativo')
			form2save = form2.save(commit=False)
			form2save.user = form.save()
			form2save.save()
			form2save.user.user_permissions.add(permission2)
			form2save.user.user_permissions.add(permission)
			return HttpResponseRedirect(self.success_url)
		else:
			return self.render_to_response(self.get_context_data(form=form, form2=form2))

class crearUsuarioEstudiante(CreateView):
	model = Curso
	second_model = Padre
	form_class = crearUsuarioUserDForm
	second_form_class = crearKardexEstudianteForm
	template_name = 'comunidad/nuevousuarioestudiante.html'
	success_url = reverse_lazy('comunidad:listausuarioestudiante')

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		if (not self.second_model.objects.all().exists()) & (not self.model.objects.all().exists()):
			context['error'] = "Debe crear cursos y usuarios de padres de familia primero, antes de registrar un nuevo estudiante."
		elif not self.second_model.objects.all().exists():
			context['error'] = "Debe crear usuarios de padres de familia primero, antes de registrar un nuevo estudiante."
		elif not self.model.objects.all().exists():
			context['error'] = "Debe crear cursos primero, antes de registrar un nuevo estudiante."
		if 'form' not in context or 'form2' not in context:
			context['form'] = self.form_class()
			context['form2'] = self.second_form_class()
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST)
		form2 = self.second_form_class(request.POST)
		if form.is_valid() and form2.is_valid():
			permission = Permission.objects.get(codename='view_estudiante')
			permission2 = Permission.objects.get(codename='view_educativo')
			form2save = form2.save(commit=False)
			form2save.user = form.save()
			form2save.save()
			form2save.user.user_permissions.add(permission2)
			form2save.user.user_permissions.add(permission)
			return HttpResponseRedirect(self.success_url)
		else:
			return self.render_to_response(self.get_context_data(form=form, form2=form2))

class updateUsuarioAdministrativo(UpdateView):
	model = get_user_model()
	second_model = Administrativo
	form_class = updateUsuarioUserForm
	second_form_class = crearKardexAdministrativoForm
	template_name = 'comunidad/nuevousuario_edit.html'
	succes_url = reverse_lazy('comunidad:listausuarioadmin')
	def get_context_data(self, **kwargs):
		context = super(updateUsuarioAdministrativo, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk',0)
		modelRes = self.model.objects.get(id=pk)
		modelRes2 = self.second_model.objects.get(user=modelRes)
		if 'form' not in context or 'form2' not in context:
			context['form'] = self.form_class(instance=modelRes)
			context['form2'] = self.second_form_class(instance=modelRes2)
		return context
	def post(self, request, *args, **kwargs):
		self.object = self.get_object	
		pk = self.kwargs.get('pk',0)
		modelRes = self.model.objects.get(id=pk)
		modelRes2 = self.second_model.objects.get(user=modelRes)
		form = self.form_class(request.POST,instance=modelRes)
		form2 = self.second_form_class(request.POST,request.FILES, instance=modelRes2)
		if form.is_valid() and form2.is_valid():
			form2Save = form2.save(commit=False)
			form2Save.user = form.save()
			form2Save.save()
			return  HttpResponseRedirect(self.succes_url)
		else:
			return self.render_to_response(self.get_context_data(form=form, form2=form2))

class updateUsuarioDocente(updateUsuarioAdministrativo):
	second_model = Docente
	second_form_class = crearKardexDocenteForm
	succes_url = reverse_lazy('comunidad:listausuariodocente')
	def get_context_data(self, **kwargs):
		context = super(updateUsuarioDocente, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk',0)
		modelRes = self.model.objects.get(id=pk)
		modelRes2 = self.second_model.objects.get(user=modelRes)
		if 'form' not in context or 'form2' not in context:
			context['form'] = self.form_class(instance=modelRes)
			context['form2'] = self.second_form_class(instance=modelRes2)
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object	
		pk = self.kwargs.get('pk',0)
		modelRes = self.model.objects.get(id=pk)
		modelRes2 = self.second_model.objects.get(user=modelRes)
		form = self.form_class(request.POST,instance=modelRes)
		form2 = self.second_form_class(request.POST,request.FILES, instance=modelRes2)
		if form.is_valid() and form2.is_valid():
			form2Save = form2.save(commit=False)
			form2Save.user = form.save()
			form2Save.save()
			form2.save_m2m()
			return  HttpResponseRedirect(self.succes_url)
		else:
			return self.render_to_response(self.get_context_data(form=form, form2=form2))

class updateUsuarioPadre(updateUsuarioAdministrativo):
	second_model = Padre
	second_form_class = crearKardexPadreForm
	template_name = 'comunidad/nuevousuario_edit.html'
	succes_url = reverse_lazy('comunidad:listausuariopadre')
	def get_context_data(self, **kwargs):
		context = super(updateUsuarioPadre, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk',0)
		modelRes = self.model.objects.get(id=pk)
		modelRes2 = self.second_model.objects.get(user=modelRes)
		if 'form' not in context or 'form2' not in context:
			context['form'] = self.form_class(instance=modelRes)
			context['form2'] = self.second_form_class(instance=modelRes2)
		return context

class updateUsuarioEstudiante(updateUsuarioAdministrativo):
	second_model = Estudiante
	second_form_class = crearKardexEstudianteForm
	template_name = 'comunidad/nuevousuario_edit.html'
	succes_url = reverse_lazy('comunidad:listausuarioestudiante')
	def get_context_data(self, **kwargs):
		context = super(updateUsuarioEstudiante, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk',0)
		modelRes = self.model.objects.get(id=pk)
		modelRes2 = self.second_model.objects.get(user=modelRes)
		if 'form' not in context or 'form2' not in context:
			context['form'] = self.form_class(instance=modelRes)
			context['form2'] = self.second_form_class(instance=modelRes2)
		return context

class updateDarBajaAdmin(UpdateView):
	model = get_user_model()
	form_class = darBajaForm
	template_name = 'comunidad/baja.html'
	success_url = reverse_lazy('comunidad:listausuarioadmin')
	def get_context_data(self, **kwargs):
		context = super(updateDarBajaAdmin, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk',0)
		user = self.model.objects.get(id=pk)
		if 'form' and 'user' not in context :
			context['form'] = self.form_class()
			context['user'] = user
		return context

class updateDarBajaDocente(UpdateView):
	model = get_user_model()
	form_class = darBajaForm
	template_name = 'comunidad/baja.html'
	success_url = reverse_lazy('comunidad:listausuariodocente')
	def get_context_data(self, **kwargs):
		context = super(updateDarBajaDocente, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk',0)
		user = self.model.objects.get(id=pk)
		if 'form' and 'user' not in context :
			context['form'] = self.form_class()
			context['user'] = user
		return context

class updateDarBajaPadre(UpdateView):
	model = get_user_model()
	form_class = darBajaForm
	template_name = 'comunidad/baja.html'
	success_url = reverse_lazy('comunidad:listausuariopadre')
	def get_context_data(self, **kwargs):
		context = super(updateDarBajaPadre, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk',0)
		user = self.model.objects.get(id=pk)
		if 'form' and 'user' not in context :
			context['form'] = self.form_class()
			context['user'] = user
		return context

class updateDarBajaEstudiante(UpdateView):
	model = get_user_model()
	form_class = darBajaForm
	template_name = 'comunidad/baja.html'
	success_url = reverse_lazy('comunidad:listausuarioestudiante')
	def get_context_data(self, **kwargs):
		context = super(updateDarBajaEstudiante, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk',0)
		user = self.model.objects.get(id=pk)
		if 'form' and 'user' not in context :
			context['form'] = self.form_class()
			context['user'] = user
		return context

class listaUsuario(ListView):
	model = get_user_model()
	form_class = searchForm
	template_name = 'comunidad/listausuario.html'

	def get_queryset(self):
		campo = None
		if self.request.method == "GET":
			form = self.form_class(self.request.GET)
			if form.is_valid():
				campo = form.cleaned_data['search']
		if not (campo):
			object_list = self.model.objects.filter(is_staff=False).order_by('id')
		return object_list

class listaAdministrativos(ListView):
	model = Administrativo
	template_name = 'comunidad/listaadministrativos.html'

class listaDocentes(ListView):
	model = Docente
	template_name = 'comunidad/listadocentes.html'

class listaPadres(ListView):
	model = Padre
	template_name = 'comunidad/listapadres.html'

class listaEstudiantes(ListView):
	model = Estudiante
	template_name = 'comunidad/listaestudiantes.html'

class listaEstudiantesCurso(ListView):
	model = Estudiante
	template_name = 'comunidad/listaestudiantes_curso.html'

	def get_queryset(self):
		pk1 = self.kwargs['pk']
		return self.model.objects.filter(curso=pk1)

class agregarPermisos(FormView):
	model = get_user_model()
	form_class = addPermissionsForm
	template_name = 'comunidad/agregarpermisos.html'
	succes_url = reverse_lazy('comunidad:listausuario')

	def get_context_data(self, **kwargs):
		context = super(agregarPermisos, self).get_context_data(**kwargs)
		pk = self.kwargs.get('pk',0)
		user = self.model.objects.get(id=pk)
		form = self.form_class(initial={'mod_comunidad':user.has_perm('auth.view_comunidad'),
										'mod_educativo':user.has_perm('auth.view_educativo')})
		if 'form' in context :
			context['form'] = form
			context['user'] = user
		return context
	def post(self, request, *args, **kwargs):
		#self.object = self.get_object	
		form = self.form_class(request.POST)
		pk = self.kwargs.get('pk',0)
		my_user = self.model.objects.get(id=pk)
		if form.is_valid():
			content_type = ContentType.objects.get_for_model(self.model)
			permission = Permission.objects.get(content_type=content_type, codename='view_personal')
			if(form.cleaned_data['mod_personal']):
				my_user.user_permissions.add(permission)
			else:
				my_user.user_permissions.remove(permission)
			permission = Permission.objects.get(content_type=content_type, codename='view_contabilidad')
			if(form.cleaned_data['mod_contabilidad']):
				my_user.user_permissions.add(permission)
			else:
				my_user.user_permissions.remove(permission)
			permission = Permission.objects.get(content_type=content_type, codename='view_cargas')
			if(form.cleaned_data['mod_cargas']):
				my_user.user_permissions.add(permission)
			else:
				my_user.user_permissions.remove(permission)
		

			return  HttpResponseRedirect(self.success_url)
		else:
			return self.render_to_response(self.get_context_data(form=form))