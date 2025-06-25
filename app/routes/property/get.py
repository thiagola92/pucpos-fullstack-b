from pydantic import BaseModel, Field
from sqlalchemy import select

from app.database import DatabaseSession
from app.database.properties import Property
from app.database.plans import Plan
from app.database.types import Type
from app.database.addresses import Address
from app.routes.property import blueprint, tag
from app.routes.generic import generic404


class PropertyGetResponse(BaseModel):
    id: int
    address_id: int
    price: int
    plan_id: int
    type_id: int
    photo: str


description = "Pega informações de um imóvel."

responses = {
    404: generic404,
    200: PropertyGetResponse,
}


class PropertyGet(BaseModel):
    id: int = Field(description="O identificador do imóvel.")


@blueprint.get("<int:id>", tags=[tag], description=description, responses=responses)
def get_property(path: PropertyGet):
    property = select(Property).where(Property.id == path.id)

    with DatabaseSession() as s:
        property = s.scalars(property).first()

        address = select(Address).where(Address.id == property.address_id)
        address = s.scalars(address).first()

        if not address:
            ("Não encontrado", 404)

        address = address.dict()

        plans = select(Plan)
        plans = s.scalars(plans).all()
        plans = {t.id: t.dict() for t in plans}

        types = select(Type)
        types = s.scalars(types).all()
        types = {p.id: p.dict() for p in types}

        property = property.dict()

        if property:
            property["plan"] = plans[property["plan_id"]]
            property["type"] = types[property["type_id"]]
            property["address"] = address

            return property

    return ("Não encontrado", 404)
