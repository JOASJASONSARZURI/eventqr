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
docker build -t qrmanager-app .
docker run -d -p 8080:8080 qrmanager-app
```

Para despliegues, configura `STORAGE_SECRET` como variable de entorno con un valor aleatorio y privado.