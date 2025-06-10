from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Property(Base):
    __tablename__ = "properties"

    id: Mapped[int] = mapped_column(primary_key=True)
    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id"), nullable=False)
