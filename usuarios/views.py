from django.shortcuts import render, redirect
from django.contrib import messages
from firebase_admin import auth, firestore
from CURSO_ingles.firebase_config import initialize_firebase
from functools import wraps
import requests
import os
from dotenv import load_dotenv
from django.views.decorators.csrf import csrf_exempt
import json # Importante para parsear el cuerpo de la petición
from django.http import JsonResponse

load_dotenv()
db = initialize_firebase()


@csrf_exempt
def api_obtener_lecciones(request):
    """API para obtener las lecciones del usuario logueado"""
    if request.method == 'GET':
        # Obtener el UID del token de Firebase
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return JsonResponse({"error": "No autenticado"}, status=401)
        
        token = auth_header[7:]  # Quitar "Bearer "
        
        try:
            # Verificar el token con Firebase Admin
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token.get('uid')
        except Exception as e:
            return JsonResponse({"error": f"Token inválido: {str(e)}"}, status=401)
        
        lecciones = []
        
        try:
            lecciones_ref = db.collection('lecciones').where('usuario_id', '==', uid).stream()
            
            for lec in lecciones_ref:
                data = lec.to_dict()
                data['id'] = lec.id
                lecciones.append(data)
                
            return JsonResponse({"lecciones": lecciones}, status=200)
            
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Método no permitido"}, status=405)


@csrf_exempt
def api_crear_leccion(request):
    """API para crear una nueva lección"""
    if request.method == 'POST':
        # Obtener el UID del token de Firebase
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return JsonResponse({"error": "No autenticado"}, status=401)
        
        token = auth_header[7:]  # Quitar "Bearer "
        
        try:
            # Verificar el token con Firebase Admin
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token.get('uid')
        except Exception as e:
            return JsonResponse({"error": f"Token inválido: {str(e)}"}, status=401)
        
        # Obtener datos del JSON
        try:
            data = json.loads(request.body)
            titulo = data.get('titulo', '').strip()
            descripcion = data.get('descripcion', '').strip()
            
            if not titulo or not descripcion:
                return JsonResponse({"error": "Título y descripción son requeridos"}, status=400)
            
            # Crear lección en Firestore
            doc_ref = db.collection('lecciones').add({
                'titulo': titulo,
                'descripcion': descripcion,
                'estado': 'Pendiente',
                'usuario_id': uid,
                'fecha_creacion': firestore.SERVER_TIMESTAMP
            })
            
            return JsonResponse({
                "mensaje": "Lección creada correctamente",
                "leccion_id": doc_ref[1].id
            }, status=201)
            
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Método no permitido"}, status=405)


# Registro de usuarios para ingresar al inicio de sesion 


def registro_usuario(request):

    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')

        try:

            # Crear usuario en Firebase
            user = auth.create_user(
                email=email,
                password=password
            )

            # Guardar perfil en Firestore
            db.collection('perfiles').document(user.uid).set({
                "uid": user.uid,
                "email": email,
                "rol": "alumno",
                "fecha_registro": firestore.SERVER_TIMESTAMP
            })

            messages.success(request, "Usuario creado correctamente")
            return redirect("login")

        except Exception as e:

            messages.error(request, f"Error: {e}")

    return render(request, "registro.html")



# Erro del registro para iniciar sesion

def login_required_firebase(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if "uid" not in request.session:

            messages.warning(request, "Debes iniciar sesión")
            return redirect("login")

        return view_func(request, *args, **kwargs)

    return wrapper


# LOGIN - inicio de sesion despues de registrarse correctamente y el logout o cerrar la sesion
@csrf_exempt
def iniciar_sesion(request):
    # --- 1. Detectar si los datos vienen de un Script (JSON) o del Navegador (POST) ---
    if request.method == 'POST':
        if request.content_type == 'application/json':
            # Si viene del script de Python
            datos = json.loads(request.body)
            email = datos.get('email')
            password = datos.get('password')
            es_api = True
        else:
            # Si viene del formulario web
            email = request.POST.get('email')
            password = request.POST.get('password')
            es_api = False

        api_key = os.getenv("FIREBASE_WEB_API_KEY")
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
        payload = {"email": email, "password": password, "returnSecureToken": True}

        try:
            response = requests.post(url, json=payload)
            data = response.json()

            if "idToken" in data: # Firebase devuelve idToken, no localId para el JWT
                # Guardar en sesión para el navegador
                request.session["uid"] = data["localId"]
                request.session["email"] = data.get("email")

                if es_api:
                    # SI ES EL SCRIPT: Devolvemos el token en JSON
                    return JsonResponse({
                        "token": data["idToken"], 
                        "email": data["email"]
                    }, status=200)
                
                # SI ES EL NAVEGADOR: Redirigimos
                uid = data["localId"]

                doc_ref = db.collection('perfiles').document(uid).get()
                perfil = doc_ref.to_dict()
                if perfil.get("rol") == "profesor":
                    return redirect("dashboard_profesor")
                else:
                    return redirect("dashboard")
            

            else:
                error_msg = data.get("error", {}).get("message", "Credenciales inválidas")
                if es_api:
                    return JsonResponse({"error": error_msg}, status=400)
                
                messages.error(request, f"Error: {error_msg}")

        except Exception as e:
            if es_api: return JsonResponse({"error": str(e)}, status=500)
            messages.error(request, f"Error: {e}")

    return render(request, "login.html")


def cerrar_sesion(request):
    request.session.flush()
    return redirect('login')



@login_required_firebase
def dashboard(request):

    uid = request.session.get('uid')
    datos_usuario = {}

    try:
        doc_ref = db.collection('perfiles').document(uid)
        doc = doc_ref.get()

        if doc.exists:
            datos_usuario = doc.to_dict()

    except Exception as e:
        messages.error(request, f"Error BD: {e}")

    # Procesar creación de nueva lección
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')

        if titulo and descripcion:
            try:
                db.collection('lecciones').add({
                    'titulo': titulo,
                    'descripcion': descripcion,
                    'estado': 'Pendiente',
                    'usuario_id': uid,
                    'fecha_creacion': firestore.SERVER_TIMESTAMP
                })

                messages.success(request, "Lección creada correctamente")
                return redirect('dashboard')
            except Exception as e:
                messages.error(request, f"Error al crear lección: {e}")
        else:
            messages.error(request, "Título y descripción son requeridos")

    # Obtener todas las lecciones del usuario
    estado_filtro = request.GET.get('estado', 'Todos')
    lecciones = []
    cursos_activos = []
    cursos_pendientes = []

    try:
        lecciones_ref = db.collection('lecciones').where('usuario_id', '==', uid).stream()

        for lec in lecciones_ref:
            data = lec.to_dict()
            data['id'] = lec.id

            # Aplicar filtro si el usuario lo seleccionó
            if estado_filtro != 'Todos' and data.get('estado') != estado_filtro:
                continue

            lecciones.append(data)
            estado = data.get('estado', 'Pendiente')

            if estado == 'Activo':
                cursos_activos.append(data)
            elif estado == 'Pendiente':
                cursos_pendientes.append(data)
    except Exception as e:
        messages.error(request, f"Error al obtener lecciones: {e}")

    return render(request, 'dashboard.html', {
        'datos': datos_usuario,
        'lecciones': lecciones,
        'cursos_activos': cursos_activos,
        'cursos_pendientes': cursos_pendientes,
        'estado_filtro': estado_filtro,
        'email': request.session.get('email')
    })


# =================
# UPDATE
# =================
@login_required_firebase
def editar_leccion(request, leccion_id):

    leccion_ref = db.collection('lecciones').document(leccion_id)

    if request.method == 'POST':
        leccion_ref.update({
            'titulo': request.POST.get('titulo'),
            'descripcion': request.POST.get('descripcion'),
            'estado': request.POST.get('estado')
        })

        messages.success(request, "Lección actualizada")
        return redirect('dashboard')

    leccion = leccion_ref.get().to_dict()
    leccion['id'] = leccion_id

    return render(request, 'editar_leccion.html', {'leccion': leccion})


# =================
# DELETE
# =================
@login_required_firebase
def eliminar_leccion(request, leccion_id):

    db.collection('lecciones').document(leccion_id).delete()
    messages.success(request, "Lección eliminada")

    return redirect('dashboard')

# =================
# Profesor
# =================

@login_required_firebase
def dashboard_profesor(request):
    uid = request.session.get('uid')
    datos_usuario = {}

    try:
        doc_ref = db.collection('perfiles').document(uid)
        doc = doc_ref.get()

        if doc.exists:
            datos_usuario = doc.to_dict()

    except Exception as e:
        messages.error(request, f"Error BD: {e}")

    lecciones = []

    try:
        lecciones_ref = db.collection('lecciones').where('usuario_id', '==', uid).stream()

        for lec in lecciones_ref:
            data = lec.to_dict()
            data['id'] = lec.id
            lecciones.append(data)

    except Exception as e:
        messages.error(request, f"Error al obtener lecciones: {e}")

   
    return render(request, 'dashboard_profesor.html', {
        'datos': datos_usuario,
        'lecciones': lecciones,
        'email': request.session.get('email')
    })