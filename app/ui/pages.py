from datetime import date
from typing import Optional

from nicegui import app, ui
from sqlmodel import Session

from app.core.database import engine
from app.repositories.attendance_repository import AttendanceRepository
from app.repositories.event_repository import EventRepository
from app.services.checkin_service import CheckInResult, CheckInService
from app.services.event_service import EventService
from app.services.export_service import ExportService
from app.services.qr_service import QRService
from app.ui.layout import frame


def _event_options(user_id: int) -> dict[int, str]:
    with Session(engine) as session:
        events = EventService(session).list_events(user_id)
        return {event.id: event.name for event in events if event.id is not None}


def _parse_date(value: Optional[str], label: str) -> date:
    if not value:
        raise ValueError(f"Indica {label}.")
    try:
        return date.fromisoformat(value)
    except ValueError as error:
        raise ValueError(f"La fecha de {label} no es válida.") from error


def render_eventos() -> None:
    if not frame("Eventos"):
        return
    user_id = int(app.storage.user["user_id"])

    ui.label("Mis eventos").classes("text-2xl font-bold")
    with ui.card().classes("w-full max-w-3xl"):
        ui.label("Crear evento").classes("text-xl font-bold")
        name_input = ui.input("Nombre del evento").classes("w-full")
        description_input = ui.input("Descripción (opcional)").classes("w-full")
        event_date_input = ui.input(
            "Fecha del evento",
            value=date.today().isoformat(),
        ).props("type=date").classes("w-full")

        with Session(engine) as session:
            initial_events = EventService(session).list_events(user_id)
        delete_options = {
            event.id: event.name
            for event in initial_events
            if event.id is not None
        }
        delete_select = ui.select(
            delete_options,
            label="Evento a borrar",
        ).classes("w-full")

        table_container = ui.column().classes("w-full")

        def refresh_events() -> None:
            with Session(engine) as session:
                events = EventService(session).list_events(user_id)
            rows = [
                {
                    "id": event.id,
                    "name": event.name,
                    "description": event.description or "",
                    "date": event.date.isoformat(),
                }
                for event in events
            ]
            table_container.clear()
            with table_container:
                ui.table(
                    columns=[
                        {"name": "name", "label": "Evento", "field": "name", "align": "left"},
                        {
                            "name": "description",
                            "label": "Descripción",
                            "field": "description",
                            "align": "left",
                        },
                        {"name": "date", "label": "Fecha", "field": "date"},
                    ],
                    rows=rows,
                    row_key="id",
                ).classes("w-full")

            delete_select.options = {
                event.id: event.name
                for event in events
                if event.id is not None
            }
            if delete_select.value not in delete_select.options:
                delete_select.value = None
            delete_select.update()

        def create_event() -> None:
            name = (name_input.value or "").strip()
            if not name:
                ui.notify("Indica el nombre del evento.", type="warning")
                return
            try:
                event_date = _parse_date(event_date_input.value, "la fecha del evento")
                with Session(engine) as session:
                    EventService(session).create_event(
                        name=name,
                        event_date=event_date,
                        user_id=user_id,
                        description=(description_input.value or "").strip() or None,
                    )
            except ValueError as error:
                ui.notify(str(error), type="warning")
                return
            name_input.value = ""
            description_input.value = ""
            refresh_events()
            ui.notify("Evento creado.", type="positive")

        def delete_event() -> None:
            if delete_select.value is None:
                ui.notify("Selecciona un evento para borrar.", type="warning")
                return
            with Session(engine) as session:
                deleted = EventService(session).delete_event(
                    int(delete_select.value),
                    user_id,
                )
            if not deleted:
                ui.notify("No se encontró el evento.", type="negative")
                refresh_events()
                return
            refresh_events()
            ui.notify("Evento eliminado.", type="positive")

        with ui.row().classes("items-center gap-3"):
            ui.button("Crear evento", on_click=create_event).props("color=primary")
            ui.button("Borrar evento seleccionado", on_click=delete_event).props(
                "color=negative outline"
            )

    ui.label("Eventos registrados").classes("text-xl font-bold mt-4")
    refresh_events()


def render_inscripcion() -> None:
    if not frame("Inscripción/QR"):
        return
    user_id = int(app.storage.user["user_id"])
    options = _event_options(user_id)

    ui.label("Inscripción de participantes").classes("text-2xl font-bold")
    if not options:
        ui.label("Primero crea un evento para poder inscribir participantes.")
        return

    with ui.card().classes("w-full max-w-2xl"):
        event_select = ui.select(
            options,
            value=next(iter(options)),
            label="Evento",
        ).classes("w-full")
        name_input = ui.input("Nombre del participante").classes("w-full")
        email_input = ui.input("Correo electrónico (opcional)").props(
            "type=email"
        ).classes("w-full")
        participant_result = ui.column().classes("w-full items-center")

        def register_participant() -> None:
            name = (name_input.value or "").strip()
            email = (email_input.value or "").strip() or None
            if not name:
                ui.notify("Indica el nombre del participante.", type="warning")
                return
            if event_select.value is None:
                ui.notify("Selecciona un evento.", type="warning")
                return
            try:
                with Session(engine) as session:
                    participant = EventService(session).register_participant(
                        event_id=int(event_select.value),
                        user_id=user_id,
                        name=name,
                        email=email,
                    )
            except ValueError as error:
                ui.notify(str(error), type="negative")
                return

            qr_base64 = QRService.generate_qr_base64(participant.token)
            qr_bytes = QRService.generate_qr_bytes(participant.token)
            participant_result.clear()
            with participant_result:
                ui.label(f"Participante inscrito: {participant.name}").classes(
                    "font-bold"
                )
                ui.image(qr_base64).classes("w-64 h-64")
                ui.label(f"Token: {participant.token}").classes(
                    "text-xs text-gray-500 break-all"
                )
                ui.button(
                    "Descargar QR (PNG)",
                    on_click=lambda: ui.download(
                        qr_bytes,
                        f"participante-{participant.id}.png",
                    ),
                ).props("color=primary")
            name_input.value = ""
            email_input.value = ""
            ui.notify("Participante inscrito y QR generado.", type="positive")

        ui.button(
            "Inscribir y generar QR",
            on_click=register_participant,
        ).props("color=primary")


def render_checkin() -> None:
    if not frame("Check-in"):
        return
    user_id = int(app.storage.user["user_id"])

    ui.label("Registrar asistencia").classes("text-2xl font-bold")
    ui.label("Escanea el QR con un lector USB o utiliza la cámara.")
    token_input = ui.input("Token del participante").props(
        "id=checkin-token"
    ).classes("w-full max-w-xl")
    ui.element("div").props("id=eventqr-camera").classes("w-full max-w-xl")

    def submit_checkin() -> None:
        token = (token_input.value or "").strip()
        if not token:
            ui.notify("Escanea o escribe un token.", type="warning")
            return
        with Session(engine) as session:
            result = CheckInService(session).check_in(token, user_id=user_id)
        notifications = {
            CheckInResult.OK: ("Asistencia registrada.", "positive"),
            CheckInResult.YA_REGISTRADO_HOY: (
                "Este participante ya está registrado hoy.",
                "warning",
            ),
            CheckInResult.TOKEN_INVALIDO: ("Token inválido.", "negative"),
        }
        message, notification_type = notifications[result]
        ui.notify(message, type=notification_type)
        token_input.value = ""

    token_input.on("keydown.enter", submit_checkin)
    ui.button(
        "Registrar asistencia",
        on_click=submit_checkin,
    ).props("id=checkin-submit color=primary")
    ui.add_body_html(
        '<script src="https://unpkg.com/html5-qrcode@2.3.8/html5-qrcode.min.js"></script>'
    )

    def start_camera() -> None:
        ui.run_javascript(
            """
            (() => {
                if (!window.Html5Qrcode) {
                    alert('No se pudo cargar el lector QR. Revisa tu conexión a Internet.');
                    return;
                }
                if (window.eventQrScanner) {
                    window.eventQrScanner.resume().catch(console.error);
                    return;
                }
                const scanner = new Html5Qrcode('eventqr-camera');
                window.eventQrScanner = scanner;
                scanner.start(
                    {facingMode: 'environment'},
                    {fps: 10, qrbox: {width: 250, height: 250}},
                    (decodedText) => {
                        const input = document.querySelector('#checkin-token input');
                        if (!input) return;
                        const setter = Object.getOwnPropertyDescriptor(
                            HTMLInputElement.prototype, 'value'
                        ).set;
                        setter.call(input, decodedText);
                        input.dispatchEvent(new Event('input', {bubbles: true}));
                        document.getElementById('checkin-submit')?.click();
                        scanner.pause(true);
                    },
                ).catch((error) => {
                    console.error(error);
                    alert('No se pudo iniciar la cámara. Verifica los permisos del navegador.');
                    window.eventQrScanner = null;
                });
            })()
            """
        )

    def stop_camera() -> None:
        ui.run_javascript(
            """
            (() => {
                if (!window.eventQrScanner) return;
                const scanner = window.eventQrScanner;
                window.eventQrScanner = null;
                scanner.stop()
                    .then(() => scanner.clear())
                    .catch(console.error);
            })()
            """
        )

    with ui.row().classes("gap-3 mt-4"):
        ui.button("Iniciar cámara", on_click=start_camera).props("outline")
        ui.button("Detener cámara", on_click=stop_camera).props("outline")


def render_reportes() -> None:
    if not frame("Reportes"):
        return
    user_id = int(app.storage.user["user_id"])
    options = _event_options(user_id)

    ui.label("Reporte de asistencias").classes("text-2xl font-bold")
    if not options:
        ui.label("No tienes eventos para consultar.")
        return

    today = date.today()
    event_select = ui.select(
        options,
        value=next(iter(options)),
        label="Evento",
    ).classes("w-full max-w-xl")
    date_from_input = ui.input(
        "Desde",
        value=today.replace(day=1).isoformat(),
    ).props("type=date")
    date_to_input = ui.input("Hasta", value=today.isoformat()).props("type=date")
    report_container = ui.column().classes("w-full")

    def get_selected_range() -> tuple[int, date, date]:
        if event_select.value is None:
            raise ValueError("Selecciona un evento.")
        start = _parse_date(date_from_input.value, "la fecha inicial")
        end = _parse_date(date_to_input.value, "la fecha final")
        if start > end:
            raise ValueError("La fecha inicial no puede ser posterior a la final.")
        return int(event_select.value), start, end

    def load_report() -> None:
        try:
            event_id, start, end = get_selected_range()
        except ValueError as error:
            ui.notify(str(error), type="warning")
            return

        with Session(engine) as session:
            event = EventRepository(session).get_event_for_user(event_id, user_id)
            if event is None:
                ui.notify("No se encontró el evento.", type="negative")
                return
            records = AttendanceRepository(session).list_for_event_date_range(
                event_id,
                start,
                end,
            )
        rows = [
            {
                "id": attendance.id,
                "participant": participant.name,
                "email": participant.email or "",
                "date": attendance.date.isoformat(),
                "time": attendance.created_at.strftime("%H:%M:%S"),
            }
            for attendance, participant in records
        ]
        report_container.clear()
        with report_container:
            ui.table(
                columns=[
                    {
                        "name": "participant",
                        "label": "Participante",
                        "field": "participant",
                        "align": "left",
                    },
                    {"name": "email", "label": "Correo", "field": "email", "align": "left"},
                    {"name": "date", "label": "Fecha", "field": "date"},
                    {"name": "time", "label": "Hora", "field": "time"},
                ],
                rows=rows,
                row_key="id",
            ).classes("w-full")

    def download_csv() -> None:
        try:
            event_id, start, end = get_selected_range()
        except ValueError as error:
            ui.notify(str(error), type="warning")
            return
        with Session(engine) as session:
            if EventRepository(session).get_event_for_user(event_id, user_id) is None:
                ui.notify("No se encontró el evento.", type="negative")
                return
            content = ExportService(session).export_attendance_csv(
                event_id,
                start,
                end,
            )
        ui.download(
            content,
            f"asistencias-{event_id}-{start.isoformat()}-{end.isoformat()}.csv",
        )

    with ui.row().classes("items-end gap-3 flex-wrap"):
        ui.button("Consultar asistencias", on_click=load_report).props("color=primary")
        ui.button("Descargar CSV", on_click=download_csv).props("outline color=primary")
