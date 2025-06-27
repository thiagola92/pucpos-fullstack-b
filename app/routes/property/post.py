from app.logger import logger

from pydantic import BaseModel
from flask import g

from app.database import DatabaseSession
from app.database.properties import Property
from app.database.property_owners import PropertyOwner
from app.database.addresses import Address
from app.routes.property import blueprint, tag, security_w
from app.routes.auth import login_required
from app.routes.util import generic_message
from app.routes.fields import PlanField, TypeField, PriceField, StreetField

description = "Cria um imóvel."

responses = {201: generic_message("property_id"), 500: {}}


class PropertyPost(BaseModel):
    street: str = StreetField
    price: int | float = PriceField
    plan_id: int = PlanField
    type_id: int = TypeField


@blueprint.post(
    "", tags=[tag], description=description, responses=responses, security=security_w
)
@login_required
def post_property(body: PropertyPost):
    try:
        with DatabaseSession() as s:
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

            property = Property(
                address_id=address.id,
                price=body.price,
                plan_id=body.plan_id,
                type_id=body.type_id,
                photo="template_house_0.svg",
            )

            s.add(property)
            s.commit()

            property_owner = PropertyOwner(
                account_id=g.account,
                property_id=property.id,
            )

            s.add(property_owner)
            s.commit()

            return (str(property.id), 201)
    except Exception as e:
        logger.error(e)
        return ("", 500)
