from django.contrib import admin

from apps.comunidad.models import *

from django.contrib.auth.admin import UserAdmin

admin.site.register(User, UserAdmin)

