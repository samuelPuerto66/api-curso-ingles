"""URL configuration for usuarios app.

This file defines all URL routes for user authentication,
dashboard, and lesson management functionality.
"""
from django.urls import path
from . import views
from .views import generar_qr

urlpatterns = [
    # ===========================================
    # AUTENTICACIÓN
    # ===========================================
    path('login/', views.iniciar_sesion, name='login'),
    path('', views.iniciar_sesion, name='login_index'),  # Página principal redirige a login
    path('registro/', views.registro_usuario, name='registro'),
    path('logout/', views.cerrar_sesion, name='cerrar_sesion'),

    # ===========================================
    # DASHBOARDS
    # ===========================================
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard-profesor/', views.dashboard_profesor, name='dashboard_profesor'),

    # ===========================================
    # GESTIÓN DE LECCIONES
    # ===========================================
    path('editar/<str:leccion_id>/', views.editar_leccion, name='editar_leccion'),
    path('eliminar/<str:leccion_id>/', views.eliminar_leccion, name='eliminar_leccion'),

    # ===========================================
    # ESTADÍSTICAS
    # ===========================================
    path('generar-qr/', generar_qr, name='generar_qr'),  # ¿Relacionado con estadísticas?
    path('estadisticas/', views.estadisticas_api, name='estadisticas'),  # Redirección o vista básica
    path('dashboard/estadisticas/', views.vista_estadisticas, name='vista_estadisticas'),  # Página HTML con gráfica

    # ===========================================
    # API ENDPOINTS (JSON responses)
    # ===========================================
    # Lecciones API
    path('api/lecciones/', views.api_obtener_lecciones, name='api_lecciones'),
    path('api/lecciones/crear/', views.api_crear_leccion, name='api_crear_leccion'),
    path('api/lecciones/editar/<str:leccion_id>/', views.api_editar_leccion, name='api_editar_leccion'),

# ===========================================
    # Estadísticas API
# ===========================================
    path('api/estadisticas/', views.estadisticas_api, name='estadisticas_api'),  # Datos JSON para gráfica
    path('api/estadisticas-datos/', views.estadisticas_api, name='estadisticas_api'),  # Alias para datos
]

