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

    try:
        with DatabaseSession() as s:
            row = s.scalars(statement).first()

            if row:
                return row.dict()
    except Exception as exception:
        print(f"{exception=}")
        return ("Error", 500)

    return ("Imóvel não encontrado", 404)
