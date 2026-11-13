**GUÍA DE LABORATORIO: QRMANAGER**

*Arquitectura Monolítica Modular en Capas con NiceGUI, SQLModel, Docker y GitHub*

<table><tbody><tr><td><p><strong>📌 OBJETIVO DE LA PRÁCTICA<br></strong>Esta guía contiene las instrucciones detalladas para empaquetar una aplicación web monolítica en Docker, configurar el archivo de documentación principal (README.md) y publicar el código fuente en GitHub directamente desde VS Code.</p></td></tr></tbody></table>

**1\. Estructura del Proyecto (Clean Architecture Monolítica)**

La aplicación sigue una separación estricta de responsabilidades dividida en 4 capas principales: Core, Modelos, Repositorios, Servicios y UI.

<table><tbody><tr><td><p>qrmanager/<br>├── .env # Variables de entorno locales<br>├── .gitignore # Archivos ignorados por Git<br>├── Dockerfile # Configuración del contenedor Docker<br>├── requirements.txt # Dependencias del proyecto<br>├── README.md # Documentación principal del repositorio<br>└── app/<br>├── main.py # Punto de entrada de la aplicación NiceGUI<br>├── core/ # Configuración, Base de datos y Seguridad (Hashing)<br>├── models/ # Definición de Entidades con SQLModel (User, QRItem)<br>├── repositories/ # Capa de Acceso a Datos (Patrón Repository)<br>├── services/ # Lógica de Negocio (Autenticación y Generación QR)<br>└── ui/ # Vistas e Interfaz de Usuario (NiceGUI)</p></td></tr></tbody></table>

**2\. Configuración e Instalación del Entorno**

**2.1. Archivo de Dependencias (requirements.txt)**

<table><tbody><tr><td><p>nicegui&gt;=2.0.0<br>sqlmodel&gt;=0.0.14<br>passlib[bcrypt]&gt;=1.7.4<br>python-dotenv&gt;=1.0.0<br>qrcode[pil]&gt;=7.4.2</p></td></tr></tbody></table>

**2.2. Variables de Entorno (.env)**

<table><tbody><tr><td><p>APP_NAME=QRManager<br>STORAGE_SECRET=qr_manager_super_secret_key_9876<br>DATABASE_URL=sqlite:///./qrmanager.db<br>PORT=8080</p></td></tr></tbody></table>

**2.3. Archivos Ignorados (.gitignore)**

<table><tbody><tr><td><p>.env<br>*.db<br>__pycache__/<br>*.pyc<br>.venv/<br>assets/qrs/</p></td></tr></tbody></table>

**3\. Creación y Despliegue del Contenedor Docker**

Docker permite empaquetar la aplicación junto con sus dependencias para garantizar su correcta ejecución en cualquier entorno.

**3.1. Archivo de Configuración (Dockerfile)**

<table><tbody><tr><td><p>FROM python:3.11-slim<br><br>WORKDIR /app<br><br>ENV PYTHONUNBUFFERED=1 \<br>PYTHONDONTWRITEBYTECODE=1<br><br>RUN apt-get update &amp;&amp; apt-get install -y --no-install-recommends \<br>build-essential \<br>&amp;&amp; rm -rf /var/lib/apt-get/lists/*<br><br>COPY requirements.txt .<br>RUN pip install --no-cache-dir -r requirements.txt<br><br>COPY app/ ./app<br>COPY .env .<br><br>EXPOSE 8080<br><br>CMD ["python", "-m", "app.main"]</p></td></tr></tbody></table>

**3.2. Comandos de Construcción y Ejecución**

Para construir la imagen Docker y levantar el contenedor, ejecuta los siguientes comandos en la terminal de tu sistema:

<table><tbody><tr><td><p># 1. Construir la imagen Docker<br>docker build -t qrmanager-app .<br><br># 2. Ejecutar el contenedor en segundo plano (puerto 8080)<br>docker run -d -p 8080:8080 --name qrmanager_container qrmanager-app</p></td></tr></tbody></table>

**4\. Creación del Archivo de Documentación (README.md)**

El archivo README.md describe las características del proyecto, la guía de instalación local y los comandos de ejecución.

<table><tbody><tr><td><p># QRManager - Sistema de Gestión y Generación de Códigos QR<br><br>QRManager es una aplicación web monolítica construida con **NiceGUI**, **SQLModel**, **SQLite**, **qrcode** y autenticación basada en sesiones.<br><br>## 🏗️ Arquitectura del Proyecto<br>El proyecto utiliza una arquitectura monolítica dividida en capas claras de presentación, lógica de negocio y persistencia de datos.<br><br>## 🚀 Requisitos Previos<br>- Python 3.11+<br>- Docker (Opcional)<br>- Git<br><br>## 🛠️ Instalación y Ejecución Local<br>1. **Clonar repositorio:** `git clone https://github.com/TU_USUARIO/qrmanager.git`<br>2. **Crear entorno virtual:** `python -m venv .venv`<br>3. **Activar entorno:** `.venv\Scripts\activate` (Windows) o `source .venv/bin/activate` (Linux/Mac)<br>4. **Instalar dependencias:** `pip install -r requirements.txt`<br>5. **Ejecutar aplicación:** `python -m app.main`<br><br>## 🐳 Ejecución con Docker<br>```bash<br>docker build -t qrmanager-app .<br>docker run -d -p 8080:8080 --name qrmanager_container qrmanager-app<br>```</p></td></tr></tbody></table>

**5\. Guía Paso a Paso para Subir el Proyecto a GitHub desde VS Code**

**Paso 1: Inicializar el Repositorio Local Git**

Abre la terminal integrada de VS Code (Ctrl + \`) en la raíz del proyecto y ejecuta:

<table><tbody><tr><td><p>git init<br>git branch -M main</p></td></tr></tbody></table>

**Paso 2: Crear el Repositorio en GitHub**

1\. Ingresa a tu cuenta de GitHub (https://github.com).  
2\. Haz clic en el botón '+' > 'New repository'.  
3\. Asigna el nombre 'qrmanager'.  
4\. Mantén desmarcadas las opciones de inicialización (sin README ni .gitignore adicionales).  
5\. Haz clic en 'Create repository' y copia la URL obtenida (HTTPS).

**Paso 3: Sincronizar y Publicar el Código**

En la terminal de VS Code, ejecuta los comandos para vincular tu repositorio local con GitHub:

<table><tbody><tr><td><p># 1. Vincular con el repositorio remoto<br>git remote add origin https://github.com/TU_USUARIO/qrmanager.git<br><br># 2. Agregar todos los archivos al área de preparación (staging)<br>git add .<br><br># 3. Registrar el primer commit<br>git commit -m "feat: initial release of QRManager with nicegui and sqlmodel"<br><br># 4. Subir los archivos a la rama main de GitHub<br>git push -u origin main</p></td></tr></tbody></table>

**Paso 4: Publicar usando la Interfaz Gráfica de VS Code (Alternativa)**

Si prefieres la interfaz gráfica de VS Code:  
1\. Ve al panel de 'Control de código fuente' (Ctrl + Shift + G).  
2\. Haz clic en el botón 'Publicar en GitHub'.  
3\. Selecciona la opción de repositorio Público o Privado.  
4\. Selecciona los archivos a incluir y confirma la publicación.