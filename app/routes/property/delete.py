from pydantic import BaseModel, Field
from sqlalchemy import select
from flask import g

from app.database import DatabaseSession
from app.database.properties import Property
from app.database.property_owners import PropertyOwner
from app.routes.property import blueprint, tag, security_w
from app.routes.auth import load_logged_in_user, login_required
from app.routes.generic import generic200, generic401


description = "Deleta um imóvel."

responses = {200: generic200, 401: generic401}


class PropertyDelete(BaseModel):
    id: int = Field(description="O Identificador do imóvel a ser deletado.")


@blueprint.delete(
    "", tags=[tag], description=description, security=security_w, responses=responses
)
@login_required
def delete_property(body: PropertyDelete):
    load_logged_in_user()

    with DatabaseSession() as s:
        property = s.get(Property, body.id)

        if not property:
            return ("Não encontrado", 404)

        owners = select(PropertyOwner).where(PropertyOwner.property_id == property.id)
        owners = s.scalars(owners).all()

        if not any([o.account_id == g.account for o in owners]):
            return ("Não autorizado", 401)

        for o in owners:
            s.delete(o)
            s.commit()

        s.delete(property)
        s.commit()

    return ("Sucesso", 200)
