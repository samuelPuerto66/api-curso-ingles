"""URL configuration for usuarios app.

This file defines all URL routes for user authentication,
dashboard, and lesson management functionality.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.iniciar_sesion, name='login'),
    path('', views.iniciar_sesion, name='login_index'),
    path('registro/', views.registro_usuario, name='registro'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('editar/<str:leccion_id>/', views.editar_leccion, name='editar_leccion'),
    path('eliminar/<str:leccion_id>/', views.eliminar_leccion, name='eliminar_leccion'),
    # API Endpoints
    path('api/lecciones/', views.api_obtener_lecciones, name='api_lecciones'),
    path('api/lecciones/crear/', views.api_crear_leccion, name='api_crear_leccion'),
]