# EventQR - Control de asistencia a eventos

Aplicación web en capas con NiceGUI, SQLModel y PostgreSQL para gestionar eventos y asistencia mediante códigos QR.

## Tecnologías
- Python 3.11+
- NiceGUI
- SQLModel
- PostgreSQL (SQLite para pruebas)
- Docker

## Funcionalidades
- Registro e inicio de sesión.
- Eventos privados por usuario.
- Inscripción de participantes y generación de QR con token UUID.
- Check-in por lector QR USB o cámara.
- Reportes de asistencia descargables en CSV compatible con Excel.

## Ejecución local
```bash
pip install -r requirements.txt
python -m app.main
```

Configura `APP_NAME`, `STORAGE_SECRET`, `DATABASE_URL` y `PORT` mediante variables de entorno o un archivo `.env` local. No publiques `.env`: contiene credenciales. La cámara requiere permiso del navegador y un contexto seguro (por ejemplo, `localhost` o HTTPS).

## Docker
```bash
docker compose up --build
```

La aplicación queda disponible en `http://localhost:8080`. Si no defines `DATABASE_URL`, Compose usa su contenedor PostgreSQL local; si la defines en `.env`, la aplicación usa esa base externa. La cuenta de base de datos debe permitir crear tablas.

## Pruebas
```bash
python -m pip install pytest
python -m pytest -q
```

## Imagen Docker independiente

```bash
docker build -t eventqr-app .
docker run -d --name eventqr-app -p 8080:8080 -e PORT=8080 -e STORAGE_SECRET="cambia-esto" -e DATABASE_URL="postgresql+psycopg://app:app@host.docker.internal:5432/eventqr" eventqr-app
```

Para despliegues, configura `STORAGE_SECRET` como variable de entorno con un valor aleatorio y privado.