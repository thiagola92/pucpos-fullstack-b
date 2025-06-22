from pydantic import BaseModel
from flask import g

from app.database import DatabaseSession
from app.database.properties import Property
from app.routes.property import blueprint, tag
from app.routes.auth import load_logged_in_user


class Body(BaseModel):
    id: int


@blueprint.delete("", tags=[tag])
def delete_property(body: Body):
    load_logged_in_user()

    if "account" not in g:
        return ("Não autenticado", 401)

    try:
        with DatabaseSession() as s:
            property = s.get(Property, body.id)

            if not property:
                return ("Imóvel não encontrado", 404)

            s.delete(property)
            s.commit()

        return ("Removido", 200)
    except Exception as exception:
        print(f"{exception=}")
        return ("Error", 500)
