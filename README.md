# 📘 PROYECTO: ACADEMY ENGLISH ONLINE 

## 📝 Descripción del proyecto

Este proyecto es una página web hecha con **Django** que sirve para gestionar un curso de inglés. Permite que los usuarios se registren, inicien sesión y puedan ver las lecciones del curso.

También está conectado con **Firebase**, que ayuda a manejar el inicio de sesión y guardar la información en la nube. La parte visual está hecha con HTML, para que el usuario pueda interactuar fácilmente con la página.

La idea principal de este proyecto es crear una plataforma sencilla para aprender inglés, mientras se ponen en práctica conocimientos básicos de programación, bases de datos y manejo de usuarios.

---

## ⚙️ Requisitos de instalación

Para poder ejecutar este proyecto en tu computador necesitas lo siguiente:

### 🐍 Versión de Python
* Tener instalado **Python 3.14.3**

### 🛠️ Herramientas necesarias
* **Django** (para crear la página web)
* **Firebase Admin SDK** (para el inicio de sesión y base de datos)
* **Virtualenv** (opcional, para organizar mejor el proyecto)
* **Git** (para descargar el proyecto)
* **SQLite3** (base de datos que usa Django)
* Un editor de código como **Visual Studio Code**


Este proyecto es una plataforma integral para la gestión de clases de inglés, que incluye un **backend web Django**, **autenticación Firebase** y un **asistente de línea de comandos con IA** integrado con Google Gemini.

---
### 🛠️ Desarrollo del Módulo de Usuarios
El sistema se construyó creando una aplicación llamada `usuarios` mediante el comando 
```
python manage.py startapp usuarios 
```
* **Interfaz:** Se diseñaron 5 vistas principales utilizando **Django Templates** y **Bootstrap 5** para la gestión de usuarios.

**Lógica:** Las vistas gestionan la autenticación mediante Firebase.


## 🛠️ Pila Tecnologica 
| Componente| Tecnologia|
| :--- | :--- |
| **Backend** | Python 3.14.3 / Django 5.2 |
| **Database** |  Firebase &  Firestore |
| **Authentication** | Firebase Admin SDK |
| **AI Integration** | Google GenAI (Gemini 2.0 Flash) |
| **Frontend** | HTML5, CSS3, Bootstrap v5.3.7 |

---

## ⚙️ Guia de instalacion

los siguientes pasos configuran el entorno de desarrollo para el proyecto.

# Crear el entorno virtual
```
python -m venv venv
```

# Activar el entorno (Windows)
```
venv\Scripts\activate
```

### instalacion  de dependencias
```
pip install -r requirements.txt
```

las Biblitecas claves incluidas fueron: Django, Firebase Admin SDK, Google GenAI y Python Dotenv, las instalaciones se hacen con el comando pip install <nombre_de_la_biblioteca>

### Configuracion de variables de entorno

crear un archivo .env en la raiz del proyecto y agregar las siguientes variables:

```env
FIREBASE_KEYS_PATH=serviceAccountKey.json
FIREBASE_WEB_API_KEY=AIzaSyBunFIgHAPiWCUPv-wH_a-BdzpvRMmQXPE
```
### configuramos el serviceAccountKey.json
```
{
  "type": "service_account",
  "project_id": "cursoingles-7e3dd",
  "private_key_id": "AIzaSyBunFIgHAPiWCUPv-wH_a-BdzpvRMmQXPE",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC2lt+45DHtIF+5\n5OJCtSe3mxMhzhpBZKiCdWDSgIgfrIFgwStmWtnn1kufSGmZ6lqtT22PhvskbgQF\nGmKdkFP1ralkeFcUJaz1/Al7/o1/obowigQCer+zzJTSqQ4mm4GNlZeV8a0jEnuo\nKwUzf9wgBhzXgki7FGv0ub/Gdr9Rgeftm+EZ7qS73lEBdv3fiJhn67JIgq9dcO4u\nB/v8A0sOxHNfFfWwQWBP4yF7s5Mz7T19g4mBh8PpMllGPZEfP1AbywBdQ2PJSwjo\n58pgbJqdX9c9p1Qirg6nWAfk231P7xYk0QDyleYiiBToGN6l8kqUSpGKEuJTo4Q7\n69lV6H7tAgMBAAECggEAAZRXXe3UFGaf4AeKa9nN0hExw+yDaSE8skOKLB/9Assh\no7Y1ZiavNQnImy7g7PosQSILWFRqVpPAuKY/B/kQOjM/oHUdtGNUC50GcaUPe8po\nxik3eimuKq5rHicPY9xGArUdJn38nwL2q2B95HFndHvLuD3csQju8HhtNS4LSczy\nYnvjy2Q9UGLPQWhi01julbSfRAsNpS502brlRRGfeldFD2lQ4I8/WIGF5x9g4bES\nPIFvyGju6/OXsWF5wky1tm4rFC8+areyqqwEUmZad3Q7CkVYYbZdbcZgPg9kjGvn\nlcntfDBSzTXJ1vf1/qFtTzoGEgr801Vzox37HOQk2QKBgQDhmEz5GX/hAi1HbjnF\nmlrOgxkQ/1DVgboa/6QBpLnucChlF07Nm4wLcR5YFNKOaSf1ePJeVbaxSA/gXjhs\nYX6XM5X0C9dZIJmzLM9PRJ2AYfMGUDlw37GapncUJTcuP8u3srHnYDNTAr5P32hE\n0nefJcIdDjpbPQmgp8yltzAJFQKBgQDPMsCc1ukyTV93SF2qL2Mt5CCTXP6p7IbU\n5zus/SKBjSZuFLtSvBuKffeXZoa0J+1j56n8xE+DC8Xfr+mI8JFqTxrkC28oJBs9\n3Ey2+oovp9MZLWCl74X3YiqWTaxjURwHKy6rCUVXFqQUPi1wDXco0oRoQuweB4lh\n33rg5AhkeQKBgQDS9V39jxfjbOq0omHJ5EbIWRXGrEqF7dL/zlEq7ESmsSFFL1+U\nq8FxLa3HhmlDnRgt15UmHBdEfvPBx7oRt7XuZOH0HmKZyP+R6vRN1wdF99KP89NT\nNwvZZ5NxNj/8stGpDaSJjo9QL/+Rp4PU38/W9jMogpaVnWV0Y5Xe3YhA5QKBgA7u\nlmj3J/kjEFU1VuKz5Y7iGOLl2ch/LjxbqbZOy9TQSku2nMVanxV8/IHhtqV3FymT\nAXIg56YHDCyRrd/bjm894i87D7ix2XC81p59McY7bwAqgAOVXm80mOMaF+lUaBOw\nLf3PfjrHe+2liXrAzayYd0hYQlHrsx/ljiJ07JHpAoGAUs0Tm3TPKnxAlGen9x6M\niMHtnLDP6WFWLC8nV6fNNOA9db44zTOW7U83k0mwuSujk3Lvjboi47w2KRcGsVaG\nrzzTpUMHZgtmXqTo1VyX5w48pAYWOwwNh3kqCi0JE6MkV64ez6U9IE5BcG9o18So\nC5sFRFnvkhmBHyUCxbwJlcU=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-fbsvc@cursoingles-7e3dd.iam.gserviceaccount.com",
  "client_id": "112828422467436199160",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40cursoingles-7e3dd.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
```

### cuentas de servicio de Firebase:

Coloca tu serviceAccountKey.json dentro del CURSO_ingles/directorio. Este archivo es esencial para firebase_config.pyinicializar el SDK de administración.

### migraciones para la base de datos
```
python manage.py makemigrations
python manage.py migrate 
```

### ejecucion de la aplicacion iniciar el servidor con Django
```
python manage.py runserver
```

### ejecucion del asistente de la linea de comandos de IA
```
python ai_cli.py
```


## 🧩 Stack Tecnológico

### 🔹 Backend (parte lógica)
- **Python 3.14.3**  
  Es el lenguaje principal del proyecto, usado para toda la lógica y funcionamiento de la aplicación.

- **Django**  
  Framework que se utilizó para crear la estructura de la página web y manejar todo el backend.

- **Django Rest Framework (DRF)**  
  Se usa para crear la API, permitiendo enviar y recibir datos en formato JSON.

---

### 🔹 Base de datos
- **PostgreSQL**  
  Base de datos donde se guarda la información del proyecto como usuarios, cursos y lecciones.

---

### 🔹 Seguridad y autenticación
- **Firebase Authentication**  
  Se encarga del registro e inicio de sesión de los usuarios.

- **Firebase Admin SDK**  
  Se usa en el servidor para validar los usuarios y controlar el acceso.

---

### 🔹 Archivos y multimedia
- **Firebase Storage / Cloudinary**  
  Se utilizan para guardar archivos como videos y audios sin cargar el servidor principal.

---

### 🔹 Herramientas de desarrollo
- **Git y GitHub**  
  Para guardar y controlar los cambios del proyecto.

- **Postman**  
  Para probar que la API funcione correctamente.

- **pip**  
  Para instalar y manejar las librerías de Python.


  # 📘 Documentación del Proyecto

## 1. 🔗 Documentación de la API

Puedes consultar la documentación completa de la API en el siguiente enlace:

https://1drv.ms/w/c/1c9ac1af828c7c0f/IQBfM60e6GD8SpQusUygFG22AX6p0wNg_QlbtxYbbwaJcdY?e=R8HtI4

---

## 2. 👥 Nombres y Cuentas

Durante el desarrollo del proyecto se presentaron algunos inconvenientes al momento de realizar los commits, lo que puede hacer que el historial sea un poco difícil de entender. A continuación, se detalla la participación de cada integrante y las cuentas utilizadas:

### 2.1 🧑‍💻 Daniel Mahecha
- Commits realizados en:
  - `Daniel444777`
  - `cabeyhonn7`
- Participación activa en ambas ramas.

---

### 2.2 🧑‍💻 Samuel Puerto
- Commits realizados en:
  - `Samuelpuerto066-afk`
  - `samuelPuerto66`
  - `Cami050`

---

### 2.3 🧑‍💻 Nicolás Salgado
- Commits realizados en:
  - `nicolassalgado147-pila`
  - `kevinmartinez13` *(algunos commits fueron subidos con esta cuenta)*

---

### 2.4 🧑‍💻 Jonathan Bernal
- ---------
- Commits realizados en:
 - `Jonathan-Bernal`
  - `Jonathan_Bernal`
  
---

## 3. ⚠️ Nota

Debido a los inconvenientes mencionados, se recomienda revisar cuidadosamente los commits para identificar correctamente la autoría y los cambios realizados.
