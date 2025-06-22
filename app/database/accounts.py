from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Account(Base):
    """
    Representa uma conta do usuário.
    """

    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(nullable=True, unique=True)
    password: Mapped[str] = mapped_column(nullable=False, unique=True)

    def dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "phone": self.phone,
            "password": self.password,
        }
