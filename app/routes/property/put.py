from app.logger import logger

from pydantic import BaseModel
from sqlalchemy import select

from app.database import DatabaseSession
from app.database.properties import Property
from app.database.addresses import Address
from app.routes.property import blueprint, tag, security_w
from app.routes.auth import login_required
from app.routes.fields import (
    PlanField,
    TypeField,
    PriceField,
    PropertyField,
    StreetField,
)

description = "Cria um imóvel."

responses = {200: {}, 404: {}, 500: {}}


class PropertyPut(BaseModel):
    id: int = PropertyField
    street: str = StreetField
    price: int | float = PriceField
    plan_id: int = PlanField
    type_id: int = TypeField


@blueprint.put(
    "", tags=[tag], description=description, responses=responses, security=security_w
)
@login_required
def put_property(body: PropertyPut):
    try:
        with DatabaseSession() as s:
            property = select(Property).where(Property.id == body.id)
            property = s.scalars(property).first()

            if not property:
                return ("", 404)

            address = select(Address).where(Address.street == body.street)
            address = s.scalars(address).first()

            if not address:
                address = Address(
                    country="Brasil",
                    state="RJ",
                    city="Rio de Janeiro",
                    street=body.street,
                    house_number=50,
                )

                s.add(address)
                s.commit()

            if isinstance(body.price, float):
                body.price = int(body.price * 100)
            else:
                body.price = body.price * 100

            property.address_id = address.id
            property.price = body.price
            property.plan_id = body.plan_id
            property.type_id = body.type_id

            s.commit()

        return ("", 200)
    except Exception as e:
        logger.error(e)
        return ("", 500)
