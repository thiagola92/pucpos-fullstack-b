from pydantic import BaseModel
from flask import g

from app.database import DatabaseSession
from app.database.properties import Property
from app.database.property_owners import PropertyOwner
from app.database.addresses import Address
from app.routes.property import blueprint, tag
from app.routes.auth import load_logged_in_user


class Body(BaseModel):
    street: str
    price: int
    plan: str


@blueprint.post("", tags=[tag])
def post_property(body: Body):
    load_logged_in_user()

    if not g.account:
        return ("Não autenticado", 401)

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

            property = Property(
                address_id=address.id,
                price=body.price,
                plan=body.plan,
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

        return ("Adicionado", 200)
    except Exception as e:
        print(e)
        return ("Error", 500)
