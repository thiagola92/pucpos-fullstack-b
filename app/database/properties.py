from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Property(Base):
    """
    Representa um imóvel e suas informações apresentadas no site.
    """

    __tablename__ = "properties"

    id: Mapped[int] = mapped_column(primary_key=True)
    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id"), nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    plan_id: Mapped[int] = mapped_column(ForeignKey("plans.id"), nullable=False)
    type_id: Mapped[int] = mapped_column(ForeignKey("types.id"), nullable=False)
    photo: Mapped[str] = mapped_column(nullable=True)

    def dict(self):
        return {
            "id": self.id,
            "address_id": self.address_id,
            "price": self.price,
            "plan_id": self.plan_id,
            "type_id": self.type_id,
            "photo": self.photo,
        }
