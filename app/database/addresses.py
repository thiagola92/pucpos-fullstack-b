from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True)
    country: Mapped[str] = mapped_column(nullable=False)
    state: Mapped[str] = mapped_column(nullable=False)
    city: Mapped[str] = mapped_column(nullable=False)
    street: Mapped[str] = mapped_column(nullable=False)
    house_number: Mapped[int] = mapped_column(nullable=False)
    extra: Mapped[str] = mapped_column()
