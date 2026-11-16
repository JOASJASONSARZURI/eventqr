from typing import List, Optional

from sqlmodel import Session, select

from app.models.entities import Event, Participant


class EventRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_event(self, event: Event) -> Event:
        self.session.add(event)
        self.session.commit()
        self.session.refresh(event)
        return event

    def get_event_by_id(self, event_id: int) -> Optional[Event]:
        return self.session.get(Event, event_id)

    def get_event_for_user(self, event_id: int, user_id: int) -> Optional[Event]:
        statement = select(Event).where(
            Event.id == event_id,
            Event.user_id == user_id,
        )
        return self.session.exec(statement).first()

    def get_events_by_user(self, user_id: int) -> List[Event]:
        statement = (
            select(Event)
            .where(Event.user_id == user_id)
            .order_by(Event.date, Event.name)
        )
        return list(self.session.exec(statement).all())

    def update_event(self, event: Event) -> Event:
        self.session.add(event)
        self.session.commit()
        self.session.refresh(event)
        return event

    def delete_event(self, event: Event) -> None:
        self.session.delete(event)
        self.session.commit()

    def create_participant(self, participant: Participant) -> Participant:
        self.session.add(participant)
        self.session.commit()
        self.session.refresh(participant)
        return participant

    def get_participant_by_id(self, participant_id: int) -> Optional[Participant]:
        return self.session.get(Participant, participant_id)

    def get_participant_by_token(
        self,
        token: str,
        user_id: Optional[int] = None,
    ) -> Optional[Participant]:
        statement = select(Participant).where(Participant.token == token)
        if user_id is not None:
            statement = statement.join(Event).where(Event.user_id == user_id)
        return self.session.exec(statement).first()

    def get_participants_by_event(self, event_id: int) -> List[Participant]:
        statement = (
            select(Participant)
            .where(Participant.event_id == event_id)
            .order_by(Participant.name)
        )
        return list(self.session.exec(statement).all())

    def update_participant(self, participant: Participant) -> Participant:
        self.session.add(participant)
        self.session.commit()
        self.session.refresh(participant)
        return participant

    def delete_participant(self, participant: Participant) -> None:
        self.session.delete(participant)
        self.session.commit()
