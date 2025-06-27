from app.logger import logger

from pydantic import BaseModel
from sqlalchemy import select

from app.database import DatabaseSession
from app.database.properties import Property
from app.database.plans import Plan
from app.database.types import Type
from app.database.addresses import Address
from app.routes.property import blueprint, tag
from app.routes.fields import PropertyField


class PropertyGetResponse(BaseModel):
    id: int
    address_id: int
    price: int
    plan_id: int
    type_id: int
    photo: str


description = "Pega informações de um imóvel."

responses = {200: PropertyGetResponse, 204: {}, 500: {}}


class PropertyGet(BaseModel):
    id: int = PropertyField


@blueprint.get("<int:id>", tags=[tag], description=description, responses=responses)
def get_property(path: PropertyGet):
    try:
        property = select(Property).where(Property.id == path.id)

        with DatabaseSession() as s:
            property = s.scalars(property).first()

            if not property:
                return ("", 204)

            address = select(Address).where(Address.id == property.address_id)
            address = s.scalars(address).first()

            if not address:
                return ("", 204)

            address = address.dict()

            plans = select(Plan)
            plans = s.scalars(plans).all()
            plans = {t.id: t.dict() for t in plans}

            types = select(Type)
            types = s.scalars(types).all()
            types = {p.id: p.dict() for p in types}

            property = property.dict()
            property["plan"] = plans[property["plan_id"]]
            property["type"] = types[property["type_id"]]
            property["address"] = address

            return property

        return ("", 204)
    except Exception as e:
        logger.error(e)
        return ("", 500)
