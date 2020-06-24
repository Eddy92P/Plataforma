# -*- coding: utf-8 -*-
from django.urls import path, re_path, include, reverse_lazy
from django.contrib import admin
from apps.comunidad.models import *
from apps.comunidad.views import *
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt


from django.contrib.auth import views as auth_views

from rest_framework import routers

urlpatterns = [
    #login_required metodo de forsado de login
    re_path(r'^$', login_required(main_page), name='main'
    ),
    path('nuevousuarioadmin/',
        #aqui el decorador de permisos
        permission_required('auth.view_comunidad')(login_required(crearUsuarioAdministrativo.as_view())), 
        name='nuevousuarioadmin'
    ),
    path('nuevousuariodocente/',
        #aqui el decorador de permisos
        permission_required('auth.view_comunidad')(login_required(crearUsuarioDocente.as_view())), 
        name='nuevousuariodocente'
    ),
    path('nuevousuariopadre/',
        #aqui el decorador de permisos
        permission_required('auth.view_comunidad')(login_required(crearUsuarioPadre.as_view())), 
        name='nuevousuariopadre'
    ),
    path('nuevousuarioestudiante/',
        #aqui el decorador de permisos
        permission_required('auth.view_comunidad')(login_required(crearUsuarioEstudiante.as_view())), 
        name='nuevousuarioestudiante'
    ),
    re_path(r'^updateusuarioadmin/(?P<pk>\d+)/$',
        permission_required('auth.view_comunidad')(login_required(updateUsuarioAdministrativo.as_view())), 
        name='updateusuarioadmin'
    ),
    re_path(r'^updateusuariodocente/(?P<pk>\d+)/$',
        permission_required('auth.view_comunidad')(login_required(updateUsuarioDocente.as_view())), 
        name='updateusuariodocente'
    ),
    re_path(r'^updateusuariopadre/(?P<pk>\d+)/$',
        permission_required('auth.view_comunidad')(login_required(updateUsuarioPadre.as_view())), 
        name='updateusuariopadre'
    ),
    re_path(r'^updateusuarioestudiante/(?P<pk>\d+)/$',
        permission_required('auth.view_comunidad')(login_required(updateUsuarioEstudiante.as_view())), 
        name='updateusuarioestudiante'
    ),
    path('listausuario/', 
        permission_required('auth.view_comunidad') (login_required(csrf_exempt(listaUsuario.as_view()))), 
        name='listausuario'
    ),
    path('listausuarioadmin/', 
        permission_required('auth.view_comunidad') (login_required(csrf_exempt(listaAdministrativos.as_view()))), 
        name='listausuarioadmin'
    ),
    path('listausuariodocente/', 
        permission_required('auth.view_comunidad') (login_required(csrf_exempt(listaDocentes.as_view()))), 
        name='listausuariodocente'
    ),
    path('listausuariopadre/', 
        permission_required('auth.view_comunidad') (login_required(csrf_exempt(listaPadres.as_view()))), 
        name='listausuariopadre'
    ),
    path('listausuarioestudiante/', 
        permission_required('auth.view_comunidad') (login_required(csrf_exempt(listaEstudiantes.as_view()))), 
        name='listausuarioestudiante'
    ),
    re_path(r'^listaestudiantes_curso/(?P<pk>\d+)/$', 
        permission_required('comunidad.view_docente') (login_required(csrf_exempt(listaEstudiantesCurso.as_view()))), 
        name='listaestudiantes_curso'
    ),
    re_path(r'^agregarpermisos/(?P<pk>\d+)/$',
        permission_required('auth.view_comunidad') (login_required(agregarPermisos.as_view())), 
        name='agregarpermisos'
    ),
    #actualisacion de cuenta por el usuario
  
    #login_required metodo de forsado de login, logout_then_login metodos de logeo de django
    path('login/', LoginView.as_view(template_name = 'comunidad/login.html'), name='login'
    ),
    path('logout/', LogoutView.as_view(), name='logout'
    ),
    path('reset_pass/',
        permission_required('comunidad.change_user')(auth_views.PasswordChangeView.as_view(template_name = 'comunidad/password_reset_form.html', success_url = '/')), name='reset_password'
    ),
    re_path(r'^darbajaadmin/(?P<pk>\d+)/$', 
        permission_required('auth.view_comunidad')(login_required(updateDarBajaAdmin.as_view())), 
        name='updatedarbajaadmin'
    ),
    re_path(r'^darbajadocente/(?P<pk>\d+)/$', 
        permission_required('auth.view_comunidad')(login_required(updateDarBajaDocente.as_view())), 
        name='updatedarbajadocente'
    ),
    re_path(r'^darbajapadre/(?P<pk>\d+)/$', 
        permission_required('auth.view_comunidad')(login_required(updateDarBajaPadre.as_view())), 
        name='updatedarbajapadre'
    ),
    re_path(r'^darbajaestudiante/(?P<pk>\d+)/$', 
        permission_required('auth.view_comunidad')(login_required(updateDarBajaEstudiante.as_view())), 
        name='updatedarbajaestudiante'
    ),
    
]
app_name = 'comunidad'