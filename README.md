# QRManager - Sistema de Gestión y Generación de Códigos QR

Aplicación web monolítica en capas desarrollada para la materia de Taller de Programación.

## Tecnologías
- Python 3.11+
- NiceGUI
- SQLModel & SQLite
- Docker

## Instalación
```bash
pip install -r requirements.txt
python -m app.main
```

Configura `APP_NAME`, `STORAGE_SECRET`, `DATABASE_URL` y `PORT` mediante variables de entorno o un archivo `.env` local. No publiques ese archivo: contiene configuración privada.

## Docker
```bash
docker compose up --build
```

La aplicación queda disponible en `http://localhost:8080` y usa un contenedor de PostgreSQL para la base de datos. Si prefieres levantar solo la imagen:

```bash
docker build -t qrmanager-app .
docker run -d --name qrmanager-app -p 8080:8080 -e PORT=8080 -e STORAGE_SECRET="cambia-esto" -e DATABASE_URL="postgresql+psycopg://app:app@host.docker.internal:5432/eventqr" qrmanager-app
```

Para despliegues, configura `STORAGE_SECRET` como variable de entorno con un valor aleatorio y privado.