# -*- coding: utf-8 -*-
from django.shortcuts import render

from django.views.generic.edit import FormMixin
from django.http import Http404
from django.utils.translation import ugettext as _

from django.views.generic import ListView, CreateView, UpdateView, FormView, DeleteView, DetailView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from apps.educativo.forms import *
from apps.educativo.models import *
from apps.comunidad.models import Estudiante, Docente, Padre
from django.db.models import Q

from django.utils import timezone
import datetime

#Auto-completado Ajax
class cursoAutocomplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		if not self.request.user.is_authenticated:
			return Curso.objects.none()
		qs = Curso.objects.filter(docente=self.request.user.id).order_by('id')
		if self.q:
			qs = qs.filter(nombre__istartswith=self.q)
		return qs

class materiaAutocomplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		if not self.request.user.is_authenticated:
			return Materia.objects.none()
		qs = Materia.objects.filter(docente=self.request.user.id).order_by('id')
		curso = self.forwarded.get('curso', None)
		if curso:
			qs = qs.filter(curso=curso)
		if self.q:
			qs = qs.filter(nombre__istartswith=self.q)
		return qs

class estudianteAutocomplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		if not self.request.user.is_authenticated:
			return Estudiante.objects.none()
		qs = Estudiante.objects.all().order_by('user_id')
		curso = self.forwarded.get('curso', None)
		if curso:
			qs = qs.filter(curso=curso)
		if self.q:
			qs = qs.filter(user__first_name__istartswith=self.q)
		return qs

#Vistas		
class crearCurso(CreateView):
	model = Curso
	form_class = crearCursoForm
	template_name = "educativo/nuevocurso.html"
	success_url = reverse_lazy("educativo:listacurso_admin")

class updateCurso(UpdateView):
	model = Curso
	form_class = crearCursoForm
	template_name = "educativo/nuevocurso.html"
	success_url = reverse_lazy("educativo:listacurso_admin")

class listaCurso(ListView):
	model = Curso
	template_name = "educativo/listacurso.html"

	def get_queryset(self):
		if self.request.user.tipo_usuario == 2:
			return self.model.objects.filter(docente=Docente.objects.get(user_id=self.request.user.id))

class listaCursoAdmin(ListView):
	model = Curso
	template_name = "educativo/listacurso_admin.html"

class crearMateria(CreateView):
	form_class = crearMateriaForm
	template_name = "educativo/nuevamateria.html"
	success_url = reverse_lazy("educativo:listamateria_admin")

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		if not Curso.objects.all().exists():
			context['error'] = "Debe crear cursos primero, antes de agregar materias."
		return context

class updateMateria(UpdateView):
	model = Materia
	form_class = crearMateriaForm
	template_name = "educativo/nuevamateria.html"
	success_url = reverse_lazy("educativo:listamateria_admin")

class listaMateria(ListView):
	model = Materia
	template_name = "educativo/listamateria.html"

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		try:
			context['curso_act'] = Curso.objects.get(id=Estudiante.objects.get(user_id=self.request.user.id).curso_id)
			context['curso_id'] = Estudiante.objects.get(user_id=self.request.user.id).curso_id
		except Exception as e:
			pass
		return context

	def get_queryset(self):
		if self.request.user.tipo_usuario == 4:
			return self.model.objects.filter(curso__id=Estudiante.objects.get(user_id=self.request.user.id).curso_id).order_by('id')

class listaMateriaAdmin(ListView):
	model = Materia
	template_name = "educativo/listamateria_admin.html"

class crearActividad(CreateView):
	form_class = crearActividadForm
	template_name = "educativo/nueva_actividad.html"
	success_url = reverse_lazy("educativo:lista_actividad")

class updateActividad(UpdateView):
	model = Actividad
	form_class = crearActividadForm
	template_name = "educativo/nueva_actividad.html"
	success_url = reverse_lazy("educativo:lista_actividad")

class listaActividad(ListView):
	model = Actividad
	template_name = "educativo/lista_actividad.html"

class crearTema(CreateView):
	model_pk = Curso
	second_model_pk = Materia
	form_class = crearTemaForm
	template_name = "educativo/nuevotema.html"
	success_url = "educativo:listatema_d"

	def get_context_data(self, **kwargs):
		context = super(crearTema, self).get_context_data(**kwargs)
		kwargs['docente'] = self.request.user
		return context

	def get_form_kwargs(self):
		kwargs = super(crearTema, self).get_form_kwargs()
		kwargs['docente'] = self.request.user
		return kwargs

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST)
		if form.is_valid():
			pk1 = self.kwargs['pk']
			materia_pk = form.cleaned_data['materia']
			num_tema = Tema.objects.filter(materia_id=materia_pk, curso_id=pk1).count()
			form = form.save(commit=False)
			form.curso_id = pk1
			if num_tema == 0:
				num_tema = 1
			else:
				num_tema += 1
			form.num_tema = num_tema
			materia = self.second_model_pk.objects.get(id=materia_pk.id)
			form.save()
			materia.save()
			return HttpResponseRedirect(reverse_lazy(self.success_url, kwargs = {'pk': pk1}))
		else:
			return self.render_to_response(self.get_context_data(form=form))

class updateTema(UpdateView):
	model = Tema
	form_class = crearTemaForm
	template_name = "educativo/nuevotema.html"
	success_url = "educativo:listatema_d"

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs['docente'] = self.request.user
		return kwargs

	def get_success_url(self):
		return reverse_lazy(self.success_url, kwargs = {'pk': self.get_object().curso_id})

class listaTemaE(ListView):
	model = Tema
	template_name = "educativo/listatema.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		pk1 = self.kwargs['pk']
		context['materia'] = Materia.objects.get(id=pk1)
		return context

	def get_queryset(self):
		pk1 = self.kwargs['pk']
		if self.request.user.tipo_usuario == 4:
			return self.model.objects.filter(curso=Estudiante.objects.get(user_id=self.request.user.id).curso_id, materia=pk1)

class listaTemaD(ListView):
	model_pk = Curso
	model = Tema
	template_name = "educativo/listatema_d.html"

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		pk1 = self.kwargs['pk']
		context['curso'] = self.model_pk.objects.get(id=pk1)
		context['pk1'] = pk1
		return context

	def get_queryset(self):
		pk1 = self.kwargs['pk']
		return self.model.objects.filter(materia__in=Materia.objects.filter(docente=self.request.user.id), curso=pk1)

"""class crearTareaEstudiante(CreateView):
	form_class = crearTareaEstudianteForm
	template_name = "educativo/nuevaentregatarea.html"
	success_url = "educativo:detalletarea"

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST, request.FILES)
		pk1 = self.kwargs['pk']
		if form.is_valid():
			form = form.save(commit=False)
			form.estudiante_id = request.user.id
			form.tarea_id = pk1
			form.entregado = True
			form.fecha_entrega = datetime.datetime.now()
			form.save()
			return HttpResponseRedirect(reverse_lazy(self.success_url, kwargs = {'pk': pk1}))
		else:
			return self.render_to_response(self.get_context_data(form=form))"""

class updateTareaEstudiante(UpdateView):
	model = Tarea_estudiante
	form_class = crearTareaEstudianteForm
	template_name = "educativo/nuevaentregatarea.html"
	success_url = "educativo:detalletarea"

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		pk1 = self.kwargs['pk']
		form = self.form_class(request.POST, request.FILES, instance=self.model.objects.get(id=pk1))
		if form.is_valid():
			form = form.save(commit=False)
			form.estudiante_id = request.user.id
			form.tarea_id = self.model.objects.get(id=pk1).tarea_id
			form.entregado = True
			form.fecha_entrega = timezone.now()
			form.save()
			return HttpResponseRedirect(reverse_lazy(self.success_url, kwargs = {'pk': self.model.objects.get(id=pk1).tarea_id}))
		else:
			return self.render_to_response(self.get_context_data(form=form))

	def get_success_url(self):
		return reverse_lazy(self.success_url, kwargs = {'pk': self.get_object().pk})

class recepcionTareaEstudiante(UpdateView):
	model = Tarea_estudiante
	form_class = recepcionTareaEstudianteForm
	template_name = "educativo/nuevaentregatarea.html"
	success_url = "educativo:listatareas_entregadas"

	def get_success_url(self):
		return reverse_lazy(self.success_url, kwargs = {'pk': self.get_object().tarea.id})

class crearTarea(CreateView):
	model = Tarea
	second_model = Tema
	form_class = crearTareaForm
	template_name = "educativo/nuevatarea.html"
	success_url = "educativo:listatarea_d"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		curso = self.kwargs['curso']
		context['curso'] = curso
		return context

	def get_form_kwargs(self):
		curso = self.kwargs['curso']
		kwargs = super().get_form_kwargs()
		kwargs['curso'] = curso
		return kwargs

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST, request.FILES)
		pk1 = self.kwargs['pk']
		curso = self.kwargs['curso']
		if form.is_valid():
			formsave = form.save(commit=False)
			formsave.tema = self.second_model.objects.get(id=pk1)
			num_tarea = self.model.objects.filter(tema_id=pk1).count()
			formsave.num_tarea = num_tarea + 1
			materia = Materia.objects.get(id=self.second_model.objects.get(id=pk1).materia_id)
			materia.save()
			formsave.docente_id = request.user.id
			formsave.save()
			form.save_m2m()
			return HttpResponseRedirect(reverse_lazy(self.success_url, kwargs = {'pk': pk1, 'curso': curso}))
		else:
			return self.render_to_response(self.get_context_data(form=form))

class updateTarea(UpdateView):
	model = Tarea
	form_class = crearTareaForm
	template_name = "educativo/nuevatarea.html"
	success_url = "educativo:listatarea_d"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		curso = self.kwargs['curso']
		pk1 = self.kwargs['pk']
		context['curso'] = curso
		context['pk1'] = pk1
		return context

	def get_form_kwargs(self):
		curso = self.kwargs['curso']
		kwargs = super().get_form_kwargs()
		kwargs['curso'] = curso
		return kwargs

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		pk1=self.kwargs['pk']
		curso=self.kwargs['curso']
		form = self.form_class(request.POST, request.FILES, instance=self.model.objects.get(id=pk1))
		if form.is_valid():
			form1 = form.save(commit=False)
			materia = Materia.objects.get(id=self.model.objects.get(id=pk1).tema.materia_id)
			materia.save()
			form1.save()
			form.save_m2m()
			return HttpResponseRedirect(reverse_lazy(self.success_url, kwargs = {'pk': self.get_object().tema.pk, 'curso': curso}))
		else:
			return self.render_to_response(self.get_context_data(form=form))

	def get_success_url(self):
		return reverse_lazy(self.success_url, kwargs = {'pk': self.get_object().tema.pk, 'curso': curso})

class listaTareaE(ListView):
	model = Tarea
	template_name = "educativo/listatarea_e.html"

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		pk1 = self.kwargs['pk']
		context['tema'] = Tema.objects.get(id=pk1)
		context['pk1'] = pk1
		return context

	def get_queryset(self):
		pk1 = self.kwargs['pk']
		return self.model.objects.filter(tema=pk1, estudiante__user_id=self.request.user.id)

class listaTareaD(ListView):
	model = Tarea
	template_name = "educativo/listatarea_d.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		curso = self.kwargs['curso']
		pk1 = self.kwargs['pk']
		context['curso'] = curso
		context['pk1'] = pk1
		context['tema'] = Tema.objects.get(id=pk1)
		return context

	def get_queryset(self):
		pk1 = self.kwargs['pk']
		return self.model.objects.filter(tema=pk1, docente__user_id=self.request.user.id)

class listaTareasEntregadasHijos(ListView):
	model = Tarea_estudiante
	template_name = "educativo/listatareas_entregadashijo.html"

	def get_queryset(self):
		return self.model.objects.filter(estudiante__in=Estudiante.objects.filter(padre=self.request.user.id))

class listaTareasEntregadas(ListView):
	model = Tarea_estudiante
	template_name = "educativo/listatareas_entregadas.html"

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		pk1 = self.kwargs['pk']
		context['tarea'] = Tarea.objects.get(id=pk1)
		context['a_tiempo'] = Tarea.objects.get(id=pk1).fecha_plazo > timezone.now()
		return context

	def get_queryset(self):
		pk1 = self.kwargs['pk']
		return self.model.objects.filter(tarea=pk1)

class detalleTarea(DetailView):
	model = Tarea
	second_model = Tarea_estudiante
	template_name = "educativo/detalletarea.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		pk1 = self.kwargs['pk']
		context['a_tiempo'] = self.model.objects.get(id=pk1).fecha_plazo > timezone.now()
		context['en_retraso'] = self.model.objects.get(id=pk1).fecha_plazo < timezone.now()
		context['tarea_e'] = self.second_model.objects.get(tarea=pk1, estudiante=self.request.user.id)

		return context

class crearMaterial(CreateView):
	model = Material
	second_model = Tema
	form_class = crearMaterialForm
	template_name = "educativo/nuevomaterial.html"
	success_url = "educativo:listamaterial_d"

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST, request.FILES)
		pk1 = self.kwargs['pk']
		if form.is_valid():
			form = form.save(commit=False)
			materia = Materia.objects.get(id=self.second_model.objects.get(id=pk1).materia_id)
			materia.save()
			form.tema_id = pk1
			form.docente_id = request.user.id
			form.save()
			return HttpResponseRedirect(reverse_lazy(self.success_url, kwargs = {'pk': pk1}))
		else:
			return self.render(self.get_context_data(form=form))

class updateMaterial(UpdateView):
	model = Material
	form_class = crearMaterialForm
	template_name = "educativo/nuevomaterial.html"
	success_url = "educativo:listamaterial_d"

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		pk1=self.kwargs['pk']
		form = self.form_class(request.POST, request.FILES, instance=self.model.objects.get(id=pk1))
		if form.is_valid():
			form1 = form.save(commit=False)
			materia = Materia.objects.get(id=self.model.objects.get(id=pk1).tema.materia_id)
			materia.save()
			form1.save()
			return HttpResponseRedirect(reverse_lazy(self.success_url, kwargs = {'pk': self.get_object().tema.pk}))
		else:
			return self.render_to_response(self.get_context_data(form=form))

	def get_success_url(self):
		return reverse_lazy(self.success_url, kwargs = {'pk': self.get_object().tema.pk})

class listaMaterial(ListView):
	model = Material
	template_name = "educativo/listamaterial.html"

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		pk1 = self.kwargs['pk']
		context['tema'] = Tema.objects.get(id=pk1)
		context['pk1'] = pk1
		return context

	def get_queryset(self):
		pk1 = self.kwargs['pk']
		return self.model.objects.filter(tema=pk1)

class listaMaterialD(listaMaterial):
	model = Material
	template_name = "educativo/listamaterial_d.html"

class crearObservacion(CreateView):
	model = Observacion
	form_class = crearObservacionForm
	template_name = "educativo/nuevaobservacion.html"
	success_url = "educativo:listatareas_entregadas"

	def get(self, request, *args, **kwargs):
		self.object = self.get_object
		try:
			pk1 = self.kwargs['pk']
			estudiante = Estudiante.objects.get(user_id=Tarea_estudiante.objects.get(id=pk1).estudiante_id)
			curso = Curso.objects.get(id=Tarea_estudiante.objects.get(id=pk1).tarea.tema.curso_id)
			materia = Materia.objects.get(id=Tarea_estudiante.objects.get(id=pk1).tarea.tema.materia_id)
			form = self.form_class(initial={'estudiante': estudiante, 'curso': curso, 'materia': materia})
		except Exception as e:
			form = self.form_class()
		return self.render_to_response(self.get_context_data(form=form))

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST)
		if form.is_valid():
			pk1 = self.kwargs['pk']
			form = form.save(commit=False)
			form.docente_id = request.user.id
			form.save()
			return HttpResponseRedirect(reverse_lazy(self.success_url, kwargs = {'pk': Tarea_estudiante.objects.get(id=pk1).tarea.id}))
		else:
			return self.render(self.get_context_data(form=form))

class crearObservacionEstudiante(CreateView):
	form_class = crearObservacionForm
	template_name = "educativo/nuevaobservacion.html"
	success_url = "educativo:listaobservacion_docente"

	def get(self, request, *args, **kwargs):
		self.object = self.get_object
		try:
			pk1 = self.kwargs['pk']
			estudiante = Estudiante.objects.get(user_id=pk1)
			curso = Curso.objects.get(id=Estudiante.objects.get(user_id=pk1).curso_id)
			form = self.form_class(initial={'estudiante': estudiante, 'curso': curso})
		except Exception as e:
			form = self.form_class()
		return self.render_to_response(self.get_context_data(form=form))

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST)
		if form.is_valid():
			pk1 = self.kwargs['pk']
			form = form.save(commit=False)
			form.docente_id = request.user.id
			form.save()
			return HttpResponseRedirect(reverse_lazy(self.success_url))
		else:
			return self.render(self.get_context_data(form=form))

class updateObservacion(UpdateView):
	model = Observacion
	form_class = crearObservacionForm
	template_name = "educativo/nuevaobservacion.html"
	success_url = reverse_lazy("educativo:listaobservacion_docente")

class listaObservacion(ListView):
	model = Observacion
	template_name = "educativo/listaobservacion.html"

	def get_queryset(self):
		return self.model.objects.filter(estudiante__in=Estudiante.objects.filter(padre=self.request.user.id))

class listaObservacionDocente(ListView):
	model = Observacion
	template_name = "educativo/listaobservacion_docente.html"

	def get_queryset(self):
		return self.model.objects.filter(docente_id=self.request.user.id)

class listaObservacionAdmin(ListView):
	model = Observacion
	template_name = "educativo/listaobservacion_admin.html"

class crearComentario(CreateView):
	form_class = crearComentarioForm
	template_name = "educativo/nuevocomentario.html"
	success_url = "educativo:listacomentario"

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST)
		if form.is_valid():
			form = form.save(commit=False)
			form.usuario_id = request.user.id
			form.save()
			return HttpResponseRedirect(reverse_lazy(self.success_url))
		else:
			return self.render(self.get_context_data(form=form))

class listaComentario(ListView):
	model = Comentario
	template_name = "educativo/listacomentario.html"

	def get_queryset(self):
		if self.request.user.tipo_usuario == 1:
			return self.model.objects.filter(Q(usuario=self.request.user.id) | Q(usuario__tipo_usuario=3))
		elif self.request.user.tipo_usuario == 3:
			return self.model.objects.filter(usuario=self.request.user.id)

class crearPension(CreateView):
	form_class = crearPensionForm
	template_name = "educativo/estadopension.html"
	success_url = "educativo:listapension"

	def post(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class(request.POST)
		if form.is_valid():
			form = form.save(commit=False)
			form.administrativo_id = request.user.id
			form.save()
			return HttpResponseRedirect(reverse_lazy(self.success_url))
		else:
			return self.render(self.get_context_data(form=form))

class updatePension(UpdateView):
	model = Pension
	form_class = crearPensionForm
	template_name = "educativo/estadopension.html"
	success_url = reverse_lazy("educativo:listapension")

class listaPension(ListView):
	model = Pension
	template_name = "educativo/listapension.html"

class listaPensionPadre(ListView):
	model = Pension
	template_name = "educativo/listapension.html"

	def get_queryset(self):
		if self.request.user.tipo_usuario == 3:
			return self.model.objects.filter(estudiante__in=Estudiante.objects.filter(padre_id=self.request.user.id))

class listaEstadoDocente(CreateView, ListView):
	model = Docente
	form_class = searchForm
	template_name = "educativo/listaestado_docente.html"

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		try:
			aux1 = self.request.GET.get('fecha1')
			aux2 = self.request.GET.get('fecha2')
			f1 = datetime.datetime.strptime(aux1, "%Y-%m-%d")
			f2 = datetime.datetime.strptime(aux2, "%Y-%m-%d")
			fecha1 = f1.strftime("%d-%m-%Y")
			fecha2 = f2.strftime("%d-%m-%Y")
			context['f1'] = self.request.GET.get('fecha1')
			context['f2'] = self.request.GET.get('fecha2')
			context['fecha1'] = fecha1
			context['fecha2'] = fecha2
		except:
			context['fecha1'] = self.request.GET.get('fecha1')
			context['fecha2'] = self.request.GET.get('fecha2')
		if 'form' not in context:
			context['form'] = self.form_class()
		return context

	def get(self, request, *args, **kwargs):
		self.object = self.get_object
		form = self.form_class()
		if request.GET:
			form = self.form_class(request.GET)
		self.object_list = self.get_queryset()
		return self.render_to_response(self.get_context_data(object_list=self.object_list , form=form))

	def get_queryset(self):
		docente = None
		if self.request.method == "GET":
			form = self.form_class(self.request.GET)
			if form.is_valid():
				docente = form.cleaned_data['docente']
		if docente:
			object_list = self.model.objects.filter(user__first_name__icontains=docente).order_by('user__first_name')
		else:
			object_list = self.model.objects.all().order_by('user__first_name')
		return object_list

class calendario_actividad(ListView):
	model = Actividad
	template_name = "educativo/calendario.html"

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		context['actividad'] = Actividad.objects.all()
		return context