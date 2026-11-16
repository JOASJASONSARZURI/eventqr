from typing import TYPE_CHECKING, List, Optional
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.entities import Event
    from app.models.qritem import QRItem


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str

    qr_items: List["QRItem"] = Relationship(back_populates="owner")
    events: List["Event"] = Relationship(back_populates="owner")