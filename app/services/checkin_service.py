from datetime import date as Date
from enum import Enum

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from app.models.entities import Attendance
from app.repositories.attendance_repository import AttendanceRepository
from app.repositories.event_repository import EventRepository


class CheckInResult(str, Enum):
    OK = "OK"
    YA_REGISTRADO_HOY = "YA_REGISTRADO_HOY"
    TOKEN_INVALIDO = "TOKEN_INVALIDO"


class CheckInService:
    def __init__(self, session: Session):
        self.session = session
        self.event_repo = EventRepository(session)
        self.attendance_repo = AttendanceRepository(session)

    def check_in(
        self,
        token: str,
        date: Date | None = None,
        user_id: int | None = None,
    ) -> CheckInResult:
        participant = self.event_repo.get_participant_by_token(
            token.strip(),
            user_id=user_id,
        )
        if participant is None or participant.id is None:
            return CheckInResult.TOKEN_INVALIDO

        attendance_date = date or Date.today()
        if self.attendance_repo.get_by_participant_and_date(
            participant.id,
            attendance_date,
        ):
            return CheckInResult.YA_REGISTRADO_HOY

        try:
            self.attendance_repo.create(
                Attendance(
                    participant_id=participant.id,
                    date=attendance_date,
                )
            )
        except IntegrityError:
            self.session.rollback()
            if self.attendance_repo.get_by_participant_and_date(
                participant.id,
                attendance_date,
            ):
                return CheckInResult.YA_REGISTRADO_HOY
            raise

        return CheckInResult.OK
