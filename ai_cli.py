import requests
import time
import getpass
import sys
import io

# Script CLI para pruebas locales

try:
    from google import genai
    from google.genai import types

    GENAI_AVAILABLE = True
except Exception:
    genai = None
    types = None
    GENAI_AVAILABLE = False

# Forzar la salida de la consola a UTF-8
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
except Exception:
    pass
# --- Configuración ---
API_KEY = "AIzaSyDlszptdn4UWlpDduKm1YIySJ7CoycwaCY"
MODELO_ID = "gemini-2.5-flash"
DEBUG_MODE = False


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
        print(
            "Error: El servidor no devolvió un JSON válido. Revisa la URL o el backend."
        )
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


def mostrar_lecciones(token_firebase: str) -> None:
    """Muestra las lecciones del usuario cuando escribe 'que lecciones tengo'"""
    url = "http://127.0.0.1:8000/api/lecciones/"
    headers = {"Authorization": f"Bearer {token_firebase}"}

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            lecciones = data.get("lecciones", [])

            if not lecciones:
                print("\n📚 No tienes lecciones creadas todavía.")
                print("   Puedes crear una desde el panel web (dashboard).")
                return

            print("\n" + "=" * 50)
            print("📚 TUS LECCIONES")
            print("=" * 50)

            for i, lec in enumerate(lecciones, 1):
                titulo = lec.get("titulo", "Sin título")
                descripcion = lec.get("descripcion", "Sin descripción")
                estado = lec.get("estado", "Pendiente")

                # Emoji según estado
                if estado == "Activo":
                    emoji = "✅"
                elif estado == "Pendiente":
                    emoji = "⏳"
                else:
                    emoji = "❓"

                print(f"\n{i}. {titulo}")
                print(f"   📝 {descripcion}")
                print(f"   {emoji} Estado: {estado}")

            print("\n" + "=" * 50)
            print(f"Total de lecciones: {len(lecciones)}")
            print("=" * 50)

        elif response.status_code == 401:
            print("\n❌ Sesión expirada. Por favor, inicia sesión nuevamente.")
        else:
            print(f"\n❌ Error al obtener lecciones: {response.status_code}")

    except Exception as e:
        print(f"\n❌ Error de conexión: {e}")

# crear una nueva lección

def crear_leccion(token_firebase: str) -> None:
    """Crea una nueva lección cuando el usuario escribe 'quiero crear una leccion nueva'"""
    print("\n📝 CREAR NUEVA LECCIÓN")
    print("-" * 30)

    titulo = input("📌 Título de la lección: ").strip()
    descripcion = input("📝 Descripción: ").strip()

    if not titulo or not descripcion:
        print("\n❌ Error: El título y la descripción son obligatorios.")
        return

    url = "http://127.0.0.1:8000/api/lecciones/crear/"
    headers = {"Authorization": f"Bearer {token_firebase}"}
    payload = {"titulo": titulo, "descripcion": descripcion}

    try:
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 201:
            data = response.json()
            print(f"\n✅ ¡Lección creada exitosamente!")
            print(f"   Título: {titulo}")
            print(f"   Estado: Pendiente (por defecto)")
        elif response.status_code == 401:
            print("\n❌ Sesión expirada. Por favor, inicia sesión nuevamente.")
        else:
            print(f"\n❌ Error al crear lección: {response.status_code}")
            print(f"   {response.text}")

    except Exception as e:
        print(f"\n❌ Error de conexión: {e}")

#ordenar  las lecciones 
def ordenar_lecciones(token_firebase: str) -> None:
    """Ordena las lecciones por estado cuando el usuario escribe 'ordena mis lecciones'"""
    url = "http://127.0.0.1:8000/api/lecciones/"
    headers = {"Authorization": f"Bearer {token_firebase}"}

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            lecciones = data.get("lecciones", [])

            if not lecciones:
                print("\n📚 No tienes lecciones para ordenar.")
                return

            # Separar por estado
            activas = [l for l in lecciones if l.get("estado") == "Activo"]
            pendientes = [l for l in lecciones if l.get("estado") == "Pendiente"]

            print("\n" + "=" * 50)
            print("📋 TUS LECCIONES ORDENADAS POR ESTADO")
            print("=" * 50)

            # Mostrar activas
            print("\n✅ LECCIONES ACTIVAS (" + str(len(activas)) + ")")
            print("-" * 40)
            if activas:
                for i, lec in enumerate(activas, 1):
                    print(f"  {i}. {lec.get('titulo', 'Sin título')}")
                    print(f"     📝 {lec.get('descripcion', '')}")
            else:
                print("  (ninguna)")

            # Mostrar pendientes
            print("\n⏳ LECCIONES PENDIENTES (" + str(len(pendientes)) + ")")
            print("-" * 40)
            if pendientes:
                for i, lec in enumerate(pendientes, 1):
                    print(f"  {i}. {lec.get('titulo', 'Sin título')}")
                    print(f"     📝 {lec.get('descripcion', '')}")
            else:
                print("  (ninguna)")

            print("\n" + "=" * 50)
            print(f"📊 Resumen: {len(activas)} activas, {len(pendientes)} pendientes")
            print("=" * 50)

        elif response.status_code == 401:
            print("\n❌ Sesión expirada. Por favor, inicia sesión nuevamente.")
        else:
            print(f"\n❌ Error al obtener lecciones: {response.status_code}")

    except Exception as e:
        print(f"\n❌ Error de conexión: {e}")

#editar lecciones 
def editar_leccion(token_firebase: str) -> None:
    """Edita una leccion existente por su ID."""
    print("\n[EDITAR LECCION]")
    id_leccion = input("ID de la leccion a editar: ").strip()
    if not id_leccion:
        return

    nuevo_titulo = input("Nuevo titulo (vacio para no cambiar): ").strip()
    nueva_desc = input("Nueva descripcion (vacio para no cambiar): ").strip()

    url = f"http://127.0.0.1:8000/api/lecciones/editar/{id_leccion}/"
    headers = {"Authorization": f"Bearer {token_firebase}"}

    payload = {}
    if nuevo_titulo:
        payload["titulo"] = nuevo_titulo
    if nueva_desc:
        payload["descripcion"] = nueva_desc

    try:
        response = requests.patch(url, json=payload, headers=headers)
        if response.status_code == 200:
            print(f"OK: Leccion {id_leccion} actualizada.")
        else:
            print(f"Error al editar: {response.status_code}")
    except Exception as e:
        print(f"Error de conexion: {e}")

#eliminar lecciones 
def eliminar_leccion(token_firebase: str) -> None:
    """Elimina una leccion por su ID."""
    print("\n[ELIMINAR LECCION]")
    id_leccion = input("ID de la leccion a borrar: ").strip()
    if not id_leccion:
        return

    confirmar = input(f"¿Seguro que quieres eliminar la leccion {id_leccion}? (s/n): ")
    if confirmar.lower() != "s":
        return

    url = f"http://127.0.0.1:8000/api/lecciones/eliminar/{id_leccion}/"
    headers = {"Authorization": f"Bearer {token_firebase}"}

    try:
        response = requests.delete(url, headers=headers)
        if response.status_code in [200, 204]:
            print(f"OK: Leccion {id_leccion} eliminada.")
        else:
            print(f"Error al eliminar: {response.status_code}")
    except Exception as e:
        print(f"Error de conexion: {e}")

#defincion de comandos 
def main() -> None:
    token = login_usuario()
    unused_var = None
    if not token:
        return

    # Inicializar cliente de IA solo si la librería está instalada y API Key válida
    client = None
    if GENAI_AVAILABLE:
        try:
            client = genai.Client(api_key=API_KEY)
        except Exception as e:
            print(f"\n⚠️ Nota: IA no disponible temporalmente ({e})")
    else:
        print(
            "\n⚠️ Nota: google.genai no está instalado. El CLI seguirá funcionando en modo lecciones."
        )

    print("\n🎓 ¡Hola! Soy tu asistente del curso de inglés.")
    print("💡 Comandos disponibles:")
    print("   • 'que lecciones tengo' - Ver todas mis lecciones")
    print("   • 'quiero crear una leccion nueva' - Crear lección")
    print("   • 'ordena mis lecciones' - Ordenar por estado")
    print("   • 'editar leccion' - Modificar una existente")
    print("   • 'eliminar leccion' - Borrar una lección")
    print("   • 'salir' - Terminar")

    while True:
        user_input = input("\nTú: ")
        if user_input.lower() in ["salir", "exit", "bye"]:
            print("¡Hasta luego! 👋")
            break

        # Normalizar el input
        input_normalizado = user_input.lower().strip()

        # === DETECTAR COMANDOS DE LECCIONES (variaciones) ===
        if (
            ("lecciones" in input_normalizado and "tengo" in input_normalizado)
            or input_normalizado == "ver mis lecciones"
            or input_normalizado == "mostrar mis lecciones"
        ):
            print("\n[SISTEMA] Cargando tus lecciones...")
            mostrar_lecciones(token)
            continue

        # === DETECTAR COMANDO: crear lección ===
        if "crear" in input_normalizado and "leccion" in input_normalizado:
            crear_leccion(token)
            continue

        # === DETECTAR COMANDO: ordenar lecciones ===
        if "ordena" in input_normalizado and "lecciones" in input_normalizado:
            print("\n[SISTEMA] Ordenando tus lecciones...")
            ordenar_lecciones(token)
            continue

        # === DETECTAR COMANDO: editar lección ===
        if "editar" in input_normalizado and "leccion" in input_normalizado:
            editar_leccion(token)
            continue

        # === DETECTAR COMANDO: eliminar lección ===
        if "eliminar" in input_normalizado or "borrar" in input_normalizado:
            eliminar_leccion(token)
            continue
        # ============================================================

        # Si no es un comando especial y la IA no está disponiblee
        if client is None:
            print("\n⚠️ Lo siento, la IA no está disponible en este momento.")
            print("   Pero puedes usar los comandos de lecciones que te mostré arriba.")
            continue

        # Construir el prompt que se envía a la IA (no afecta lógica de comandos)
        prompt = (
            f"Instrucción: Eres un asistente para ADSO. "
            f"Para cualquier consulta técnica, utiliza EXCLUSIVAMENTE este token de Firebase: {token}. "
            "IMPORTANTE: No uses tu propia API Key. "
            f"Pregunta del usuario: {user_input}"
        )

        try:
            # Llamada compatible con la API de google.genai
            response = client.models.generate_content(
                model=MODELO_ID,
                contents=[types.TextContent(text=prompt)],
            )

            if hasattr(response, "output") and response.output:
                ia_text = response.output[0].content[0].text
            else:
                ia_text = getattr(response, "text", str(response))

            print(f"IA: {ia_text}")
        except Exception as e:
            error_str = str(e)
            if "403" in error_str and "leaked" in error_str:
                print("⚠️ La IA está temporalmente indisponible.")
                print("   Pero puedes usar los comandos de lecciones:")
                print("   • 'que lecciones tengo'")
                print("   • 'quiero crear una leccion nueva'")
                print("   • 'ordena mis lecciones'")
                print("   • 'editar leccion'")
                print("   • 'eliminar leccion'")
            elif "429" in error_str:
                print(
                    "IA: Agotamos las peticiones gratuitas del minuto. Espera 20 segundos..."
                )
                time.sleep(20)
            elif "404" in error_str:
                print("IA: Error de versión de modelo. Intentando reconectar...")
            else:
                print(f"Ups! Algo pasó: {e}")
if __name__ == "__main__":
    main()