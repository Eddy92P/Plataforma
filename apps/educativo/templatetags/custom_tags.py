from django import template
from apps.educativo.models import *

register = template.Library()

@register.simple_tag
def tema(Materia, Curso, f1, f2):	
	return Materia.temas(Curso, f1, f2)

@register.simple_tag
def tarea(Materia, f1, f2):	
	return Materia.tareas(f1, f2)

@register.simple_tag
def doc_encargado(Materia, curso_id):	
	return Materia.docente_encargado(curso_id)