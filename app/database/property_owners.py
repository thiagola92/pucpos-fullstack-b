from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class PropertyOwner(Base):
    __tablename__ = "property_owners"

    id: Mapped[int] = mapped_column(primary_key=True)
    person_id: Mapped[int] = mapped_column(ForeignKey("properties.id"))
    property_id: Mapped[int] = mapped_column(ForeignKey("persons.id"))
