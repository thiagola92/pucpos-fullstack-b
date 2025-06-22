from pydantic import BaseModel
from sqlalchemy import select

from app.database import DatabaseSession
from app.database.properties import Property
from app.routes.property import blueprint, tag


class Path(BaseModel):
    id: int


@blueprint.get("<int:id>", tags=[tag])
def get_property(path: Path):
    statement = select(Property).where(Property.id == path.id)

    with DatabaseSession() as s:
        row = s.scalars(statement).first()

        if row:
            return row.dict()

    return ("Imóvel não encontrado", 404)
