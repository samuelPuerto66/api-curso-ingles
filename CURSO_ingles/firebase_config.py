"""Configuración e inicialización de Firebase para el proyecto.

Este módulo carga las variables de entorno desde el archivo .env en la raíz
del proyecto y expone una función para inicializar Firebase Admin con la llave
de servicio.
"""

import os
from pathlib import Path
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# Cargar variables de entorno desde el .env de la raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

def initialize_firebase():
    """Inicializa el SDK de Firebase Admin si no está ya inicializado."""

    if not firebase_admin._apps:
        try:
            # Obtener el nombre del archivo desde el .env o usar el valor por defecto
            file_name = os.getenv("FIREBASE_KEYS_PATH", "serviceAccountKey.json")
            cert_path = BASE_DIR / file_name

            if not cert_path.exists():
                raise FileNotFoundError(f"No se encontró el archivo de credenciales en: {cert_path}")

            # Inicialización
            cred = credentials.Certificate(str(cert_path))
            firebase_admin.initialize_app(cred)
            print(f"✅ Firebase SDK inicializado correctamente usando: {file_name}")
            
        except Exception as e:
            print(f"❌ Error crítico al inicializar Firebase: {e}")
            return None

    # Retorna el cliente de Firestore
    return firestore.client()

# Ejemplo de uso (puedes comentar esto en producción)
if __name__ == "__main__":
    db = initialize_firebase()
    if db:
        print("🚀 Conexión a Firestore lista para usar.")