
# 🩺 MediCita — Sistema de Gestión de Citas Médicas

MediCita es una aplicación web desarrollada con **Python y Django** que permite gestionar citas médicas, consultar profesionales de salud y facilitar la organización de la atención médica.

## ✨ Funcionalidades principales

- 👤 Registro e inicio de sesión de usuarios.
- 🩺 Consulta y búsqueda de médicos.
- 📅 Agendamiento de citas médicas.
- 🔄 Reprogramación de citas.
- ❌ Cancelación de citas.
- 📋 Consulta de citas programadas.
- 🏥 Información de centros médicos y especialidades.
- 💬 Sección de chatbot.
- 📊 Vista de información demográfica.
- 🔐 Administración de usuarios mediante Django.
- 🧪 Generación de datos de demostración para realizar pruebas.

## 🛠️ Tecnologías utilizadas

| Tecnología | Descripción |
|---|---|
| Python | Lenguaje de programación |
| Django | Framework para el desarrollo web |
| SQLite | Base de datos local |
| HTML | Estructura de las páginas |
| CSS | Diseño y estilos |
| Git y GitHub | Control de versiones y alojamiento del código |

## 📂 Estructura del proyecto

```text
MediCita/
├── citas/
│   ├── management/
│   │   └── commands/
│   │       └── seed.py
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   ├── admin.py
│   ├── models.py
│   ├── triage.py
│   ├── urls.py
│   └── views.py
├── config/
│   ├── settings.py
│   └── urls.py
├── manage.py
├── requirements.txt
└── README.md
```

## 💻 Requisitos

Antes de ejecutar el proyecto, asegúrate de tener instalado:

- Python 3.10 o superior.
- pip.
- Visual Studio Code (recomendado).
- Git (opcional, para clonar el repositorio).

## 🚀 Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/yeris01/MediCita.git
cd medicita
```

Reemplaza `https://github.com/yeris01/MediCita.git` por la dirección de tu repositorio de GitHub.

### 2. Crear el entorno virtual

En Windows, abre la terminal de Visual Studio Code y ejecuta:

```powershell
py -m venv venv
```

### 3. Activar el entorno virtual

```powershell
.\venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación, ejecuta:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Después, vuelve a activar el entorno virtual.

### 4. Instalar las dependencias

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Preparar la base de datos

```bash
python manage.py migrate
```

### 6. Cargar datos de demostración

```bash
python manage.py seed
```

Este comando permite generar datos de prueba para explorar las funcionalidades de la aplicación.

### 7. Ejecutar el servidor

```bash
python manage.py runserver
```

Abre el navegador en:

**http://127.0.0.1:8000/**

## 🌐 Rutas principales

| Ruta | Función |
|---|---|
| `/` | Página principal y búsqueda de médicos |
| `/login/` | Inicio de sesión |
| `/logout/` | Cierre de sesión |
| `/registro/` | Registro de usuarios |
| `/mis-citas/` | Consulta de citas |
| `/demografia/` | Información demográfica |
| `/chatbot/` | Sección de chatbot |
| `/admin/` | Panel de administración |

## 🔑 Credenciales de demostración

Para realizar pruebas locales, después de ejecutar el comando de carga de datos:

| Perfil | Usuario | Contraseña |
|---|---|---|
| Administrador | `admin` | `admin123` |
| Pacientes de prueba | `paciente1` a `paciente30` | `demo1234` |

**Importante:** estas credenciales son únicamente para demostración. No deben utilizarse en un entorno de producción.

## ⚙️ Comandos útiles de Django

Comprobar la configuración:

```bash
python manage.py check
```

Crear migraciones después de modificar los modelos:

```bash
python manage.py makemigrations
python manage.py migrate
```

Crear un administrador:

```bash
python manage.py createsuperuser
```

Detener el servidor:

```text
Ctrl + C
```

## 🔒 Seguridad

Antes de desplegar MediCita en producción:

- Configura una clave secreta segura mediante variables de entorno.
- Desactiva `DEBUG`.
- Configura `ALLOWED_HOSTS`.
- No publiques contraseñas, archivos `.env` ni datos personales.
- Utiliza HTTPS y una configuración segura de la base de datos.
- Evita utilizar información médica real en los datos de demostración.

## 👩‍💻 Desarrollo

MediCita es un proyecto orientado a la gestión de citas médicas y a la organización de la información relacionada con pacientes y profesionales de salud.

Para contribuir:

1. Crea una rama para tus modificaciones.
2. Implementa y prueba tus cambios.
3. Verifica la configuración con `python manage.py check`.
4. Realiza un commit y envía los cambios a GitHub.

---

**MediCita 🩺**  
*Tecnología para facilitar la gestión de citas médicas.*
