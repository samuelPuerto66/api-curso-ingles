import requests
import time
import getpass
from google import genai
from google.genai import types

# --- Configuración ---
API_KEY = "AIzaSyD1oRY5_Ut1dT3L73tj-c752yfDMMTzA18"
MODELO_ID = "gemini-2.5-flash"


def login_usuario() -> str | None:
    print("--- Login de Aprendiz/Instructor ---")
    email = input("Email: ")
    password = getpass.getpass("Contraseña: ")

    url_login = "http://127.0.0.1:8000/login/"
    payload = {"email": email, "password": password}

    try:
        response = requests.post(url_login, json=payload)
        
        # 1. Verificar si la respuesta fue exitosa (200 OK)
        if response.status_code == 200:
            data = response.json()
            print("Autenticación exitosa.")
            return data.get("token")
        else:
            # 2. Si no es 200, mostramos qué devolvió el servidor en vez de crashear
            print(f"Error {response.status_code}: {response.text}")
            return None

    except requests.exceptions.JSONDecodeError:
        print("Error: El servidor no devolvió un JSON válido. Revisa la URL o el backend.")
    except Exception as e:
        print(f"Error de conexión: {e}")

    return None


def consultar_mis_tareas(token_firebase: str) -> dict:
    """Consulta las tareas del usuario logueado en la API de Django."""

    print("\n[SISTEMA] Consultando API de Django...")
    url = "http://127.0.0.1:8000/dashboard/"
    headers = {"Authorization": f"Bearer {token_firebase}"}

    try:
        res = requests.get(url, headers=headers)
        return res.json()
    except Exception as e:
        return {"error": str(e)}


def main() -> None:
    token = login_usuario()
    if not token:
        return

    client = genai.Client(api_key=API_KEY)

    print("\nIA: ¡Hola! Soy tu asistente de ADSO. ¿Qué deseas consultar hoy?")

    while True:
        user_input = input("\nTú: ")
        if user_input.lower() in ["salir", "exit", "bye"]:
            break

        prompt = (
            f"Instrucción: Eres un asistente para ADSO. "
            f"Para cualquier consulta técnica, utiliza EXCLUSIVAMENTE este token de Firebase: {token}. "
            "IMPORTANTE: No uses tu propia API Key. "
            f"Pregunta del usuario: {user_input}"
        )

        try:
            # CAMBIO: Cambiamos 'prompt' por 'contents'
            response = client.models.generate_content(
             model=MODELO_ID,
                contents=prompt,
                config=types.GenerateContentConfig(
                tools=[consultar_mis_tareas]
            ),
        )

            print(f"IA: {response.text}")
        except Exception as e:
            error_str = str(e)
            if "429" in error_str:
                print("IA: Agotamos las peticiones gratuitas del minuto. Espera 20 segundos...")
                time.sleep(20)
            elif "404" in error_str:
                print("IA: Error de versión de modelo. Intentando reconectar...")
            else:
                print(f"Ups! Algo pasó: {e}")


if __name__ == "__main__":
    main()
