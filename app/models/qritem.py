from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.user import User


class QRItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    data_content: str
    category: str = "General"
    
    user_id: int = Field(foreign_key="user.id")
    owner: Optional["User"] = Relationship(back_populates="qr_items")