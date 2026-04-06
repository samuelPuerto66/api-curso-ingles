import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# Importamos las rutas de websocket de tu app usuarios
import usuarios.routing 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CURSO_ingles.settings')

application = ProtocolTypeRouter({
    # Para peticiones normales (las páginas web)
    "http": get_asgi_application(),
    
    # Para el chat en tiempo real
    "websocket": AuthMiddlewareStack(
        URLRouter(
            usuarios.routing.websocket_urlpatterns
        )
    ),
})