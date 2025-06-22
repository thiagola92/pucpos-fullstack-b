from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Plan(Base):
    """
    Armazena as possíveis ações que o usuário pode querer para o imóvel
    dentro da plataforma.

    1- Vender
    2- Alugar
    """

    __tablename__ = "plans"

    id: Mapped[int] = mapped_column(primary_key=True)
    plan: Mapped[str] = mapped_column(nullable=False, unique=True)

    def dict(self):
        return {
            "id": self.id,
            "plan": self.plan,
        }
