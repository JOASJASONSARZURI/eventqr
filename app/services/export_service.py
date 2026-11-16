import csv
import io
from datetime import date

from sqlmodel import Session

from app.repositories.attendance_repository import AttendanceRepository


class ExportService:
    def __init__(self, session: Session):
        self.attendance_repo = AttendanceRepository(session)

    def export_attendance_csv(
        self,
        event_id: int,
        date_from: date,
        date_to: date,
    ) -> bytes:
        if date_from > date_to:
            raise ValueError("La fecha inicial no puede ser posterior a la final.")

        records = self.attendance_repo.list_for_event_date_range(
            event_id,
            date_from,
            date_to,
        )
        output = io.StringIO(newline="")
        writer = csv.writer(output)
        writer.writerow(["Participante", "Correo", "Fecha", "Hora"])
        for attendance, participant in records:
            writer.writerow(
                [
                    participant.name,
                    participant.email or "",
                    attendance.date.isoformat(),
                    attendance.created_at.strftime("%H:%M:%S"),
                ]
            )
        return output.getvalue().encode("utf-8-sig")
