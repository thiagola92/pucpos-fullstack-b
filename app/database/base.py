# Separated to avoid circular imports.
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
