from pydantic import BaseModel

from app.database import DatabaseSession
from app.database.properties import Property
from app.routes.property import blueprint, tag


class Body(BaseModel):
    id: int


@blueprint.delete("", tags=[tag])
def delete_property(body: Body):
    try:
        with DatabaseSession() as s:
            property = s.get(Property, body.id)

            if not property:
                return ("Imóvel não encontrado", 404)

            s.delete(property)
            s.commit()

        return ("Removido", 200)
    except Exception as e:
        print(e)
        return ("Error", 500)
