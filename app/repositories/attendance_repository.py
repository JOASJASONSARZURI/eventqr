from datetime import date
from typing import List, Optional, Tuple

from sqlmodel import Session, select

from app.models.entities import Attendance, Participant


class AttendanceRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, attendance: Attendance) -> Attendance:
        self.session.add(attendance)
        self.session.commit()
        self.session.refresh(attendance)
        return attendance

    def get_by_participant_and_date(
        self,
        participant_id: int,
        attendance_date: date,
    ) -> Optional[Attendance]:
        statement = select(Attendance).where(
            Attendance.participant_id == participant_id,
            Attendance.date == attendance_date,
        )
        return self.session.exec(statement).first()

    def list_for_event_date_range(
        self,
        event_id: int,
        date_from: date,
        date_to: date,
    ) -> List[Tuple[Attendance, Participant]]:
        statement = (
            select(Attendance, Participant)
            .join(Participant, Attendance.participant_id == Participant.id)
            .where(
                Participant.event_id == event_id,
                Attendance.date >= date_from,
                Attendance.date <= date_to,
            )
            .order_by(Attendance.date, Attendance.created_at, Participant.name)
        )
        return list(self.session.exec(statement).all())
