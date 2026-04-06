"""URL configuration for usuarios app.

This file defines all URL routes for user authentication,
dashboard, and lesson management functionality.
"""
from django.urls import path
from . import views
from .views import generar_qr

urlpatterns = [
    path('login/', views.iniciar_sesion, name='login'),
    path('', views.iniciar_sesion, name='login_index'),
    path('registro/', views.registro_usuario, name='registro'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('generar-qr/', generar_qr, name='generar_qr'),
    path('logout/', views.cerrar_sesion, name='cerrar_sesion'),
    path('editar/<str:leccion_id>/', views.editar_leccion, name='editar_leccion'),
    path('eliminar/<str:leccion_id>/', views.eliminar_leccion, name='eliminar_leccion'),
    path('dashboard-profesor/', views.dashboard_profesor, name='dashboard_profesor'),
    # API Endpoints
    path('api/lecciones/', views.api_obtener_lecciones, name='api_lecciones'),
    path('api/lecciones/crear/', views.api_crear_leccion, name='api_crear_leccion'),
    path('api/lecciones/editar/<str:leccion_id>/', views.api_editar_leccion, name='api_editar_leccion'),
]
