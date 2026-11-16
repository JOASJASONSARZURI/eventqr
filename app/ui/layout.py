from nicegui import app, ui


NAVIGATION = (
    ("Eventos", "/eventos"),
    ("Inscripción/QR", "/inscripcion"),
    ("Check-in", "/checkin"),
    ("Reportes", "/reportes"),
)


def frame(titulo: str) -> bool:
    user = app.storage.user
    user_id = user.get("user_id")
    if not user.get("authenticated", False) or user_id is None:
        ui.navigate.to("/")
        return False

    def logout() -> None:
        app.storage.user.clear()
        ui.navigate.to("/")

    with ui.header().classes(
        "items-center justify-between gap-4 flex-wrap bg-gray-800 text-white p-4 shadow"
    ):
        ui.label(f"EventQR | {titulo}").classes("text-lg font-bold")
        with ui.row().classes("items-center gap-4 flex-wrap"):
            for label, route in NAVIGATION:
                ui.link(label, route).classes("text-white")
            ui.label(str(user.get("username", ""))).classes("font-medium")
            ui.button("Cerrar sesión", on_click=logout).props("flat color=white")
    return True
