from django.apps import AppConfig


class UsuariosConfig(AppConfig):
    """
    Configuración de la aplicación de usuarios.
    
    Esta clase define la configuración principal para la app 'usuarios'
    que maneja la autenticación, registro y gestión de usuarios.
    """
    name = 'usuarios'
    verbose_name = 'Gestión de Usuarios'
