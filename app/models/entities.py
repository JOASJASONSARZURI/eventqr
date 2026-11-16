from datetime import date, datetime
from typing import TYPE_CHECKING, List, Optional
from uuid import uuid4

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.user import User


class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    date: date
    user_id: int = Field(foreign_key="user.id", index=True)

    owner: Optional["User"] = Relationship(back_populates="events")
    participants: List["Participant"] = Relationship(
        back_populates="event",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class Participant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    event_id: int = Field(foreign_key="event.id", index=True)
    name: str
    email: Optional[str] = None
    token: str = Field(
        default_factory=lambda: str(uuid4()),
        unique=True,
        index=True,
    )

    event: Optional["Event"] = Relationship(back_populates="participants")
    attendances: List["Attendance"] = Relationship(
        back_populates="participant",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class Attendance(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("participant_id", "date"),)

    id: Optional[int] = Field(default=None, primary_key=True)
    participant_id: int = Field(foreign_key="participant.id", index=True)
    date: date
    created_at: datetime = Field(default_factory=datetime.now)

    participant: Optional["Participant"] = Relationship(back_populates="attendances")
