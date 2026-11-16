from datetime import date
from typing import List, Optional
from uuid import uuid4

from sqlmodel import Session

from app.models.entities import Event, Participant
from app.repositories.event_repository import EventRepository


class EventService:
    def __init__(self, session: Session):
        self.repo = EventRepository(session)

    def create_event(
        self,
        name: str,
        event_date: date,
        user_id: int,
        description: Optional[str] = None,
    ) -> Event:
        event = Event(
            name=name,
            date=event_date,
            user_id=user_id,
            description=description,
        )
        return self.repo.create_event(event)

    def list_events(self, user_id: int) -> List[Event]:
        return self.repo.get_events_by_user(user_id)

    def delete_event(self, event_id: int, user_id: int) -> bool:
        event = self.repo.get_event_for_user(event_id, user_id)
        if event is None:
            return False
        self.repo.delete_event(event)
        return True

    def register_participant(
        self,
        event_id: int,
        user_id: int,
        name: str,
        email: Optional[str] = None,
    ) -> Participant:
        if self.repo.get_event_for_user(event_id, user_id) is None:
            raise ValueError("Evento no encontrado.")

        participant = Participant(
            event_id=event_id,
            name=name,
            email=email,
            token=str(uuid4()),
        )
        return self.repo.create_participant(participant)

    def list_participants(self, event_id: int, user_id: int) -> List[Participant]:
        if self.repo.get_event_for_user(event_id, user_id) is None:
            raise ValueError("Evento no encontrado.")
        return self.repo.get_participants_by_event(event_id)
