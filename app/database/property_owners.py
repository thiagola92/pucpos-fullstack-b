from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class PropertyOwner(Base):
    __tablename__ = "property_owners"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    property_id: Mapped[int] = mapped_column(ForeignKey("properties.id"))
