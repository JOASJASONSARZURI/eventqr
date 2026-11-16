from nicegui import ui
# Import the mapped classes before init_db reads SQLModel metadata.
from app.models import entities  # pyright: ignore[reportUnusedImport]
from app.core.config import settings
from app.core.database import init_db
from app.ui.auth_pages import render_login, render_register
from app.ui.dashboard_pages import render_dashboard
from app.ui.pages import (
    render_checkin,
    render_eventos,
    render_inscripcion,
    render_reportes,
)

init_db()

@ui.page('/')
def login_page():
    render_login()

@ui.page('/register')
def register_page():
    render_register()

@ui.page('/dashboard')
def dashboard_page():
    render_dashboard()

@ui.page('/eventos')
def eventos_page():
    render_eventos()

@ui.page('/inscripcion')
def inscripcion_page():
    render_inscripcion()

@ui.page('/checkin')
def checkin_page():
    render_checkin()

@ui.page('/reportes')
def reportes_page():
    render_reportes()

if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        title=settings.APP_NAME,
        host="0.0.0.0",
        port=settings.PORT,
        storage_secret=settings.STORAGE_SECRET,
        reload=False
    )