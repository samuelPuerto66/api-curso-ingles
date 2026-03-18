#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.

Este script permite ejecutar comandos de gestión de Django
como migraciones, servidor de desarrollo, creación de superusuarios, etc.
"""
import os
import sys


def main():
    """
    Ejecuta las tareas administrativas de Django.
    
    Configura el módulo de settings y ejecuta los comandos
    recibidos desde la línea de comandos.
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CURSO_ingles.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()


