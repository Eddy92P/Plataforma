
from __future__ import unicode_literals

from django.apps import AppConfig


class ComunidadConfig(AppConfig):
    name = 'comunidad'

def create_perms():
	from django.contrib.auth.models import User
	from django.contrib.auth.models import Permission
	from django.contrib.contenttypes.models import ContentType
	try:
		content_type = ContentType.objects.get_for_model(User)
		permission = Permission.objects.create(
			codename='view_educativo',
			name='Ver educativo',
			content_type=content_type,
		)
	except:
		print ("permiso 1 ya aderido")
	try:
		content_type = ContentType.objects.get_for_model(User)
		permission = Permission.objects.create(
			codename='view_comunidad',
			name='Ver comunidad',
			content_type=content_type,
		)
	except:
		print ("permiso 2 ya aderido")