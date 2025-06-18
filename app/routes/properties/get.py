from sqlalchemy import select

from app.database import DatabaseSession
from app.database.properties import Property
from app.routes.properties import blueprint, tag


@blueprint.get("", tags=[tag])
def get_properties():
    statement = select(Property)

    with DatabaseSession() as s:
        rows = s.scalars(statement).all()

        if rows:
            return [r.dict() for r in rows]

    return ("Error", 500)
