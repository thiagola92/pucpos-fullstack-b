from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class PropertyOwner(Base):
    """
    Representa a relação de um imóvel com múltiplos donos.

    Pense no caso dos seus filhos herdarem o seu imóvel,
    todos eles são parcialmente donos do imóvel.

    O plano seria deixar uma conta adicionar o imóvel e
    depois ela linkar a outras contas.
    """

    __tablename__ = "property_owners"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    property_id: Mapped[int] = mapped_column(ForeignKey("properties.id"))
