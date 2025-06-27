from app.logger import logger

from pydantic import BaseModel
from sqlalchemy import select
from flask import g

from app.database import DatabaseSession
from app.database.properties import Property
from app.database.property_owners import PropertyOwner
from app.routes.property import blueprint, tag, security_w
from app.routes.auth import login_required
from app.routes.fields import PropertyField


description = "Deleta um imóvel."

responses = {200: {}, 204: {}, 401: {}, 500: {}}


class PropertyDelete(BaseModel):
    id: int = PropertyField


@blueprint.delete(
    "", tags=[tag], description=description, security=security_w, responses=responses
)
@login_required
def delete_property(body: PropertyDelete):
    try:
        with DatabaseSession() as s:
            property = s.get(Property, body.id)

            if not property:
                return ("", 204)

            owners = select(PropertyOwner).where(
                PropertyOwner.property_id == property.id
            )
            owners = s.scalars(owners).all()

            if not any([o.account_id == g.account for o in owners]):
                return ("", 401)

            for o in owners:
                s.delete(o)
                s.commit()

            s.delete(property)
            s.commit()

        return ("", 200)
    except Exception as e:
        logger.error(e)
        return ("", 500)
