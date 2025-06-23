from sqlalchemy import select

from app.database import DatabaseSession
from app.database.types import Type
from app.routes.types import blueprint, tag


@blueprint.get("", tags=[tag])
def get_type():
    with DatabaseSession() as s:
        types = select(Type)
        types = s.scalars(types).all()
        types = [p.dict() for p in types]

        return types
