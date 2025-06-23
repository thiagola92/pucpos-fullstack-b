from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Type(Base):
    """
    Armazena as possíveis tipos de imóveis.

    1- Casa
    2- Apartamento
    """

    __tablename__ = "types"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }
