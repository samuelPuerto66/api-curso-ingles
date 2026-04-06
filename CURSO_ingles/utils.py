import socket

def get_local_ip():
    """Detecta la IP privada actual del computador."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # No realiza una conexión real, solo detecta la interfaz activa
        s.connect(('8.8.8.8', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip