from sqlalchemy import select
from pydantic import BaseModel

from app.database import DatabaseSession
from app.database.properties import Property
from app.database.addresses import Address
from app.routes.property import blueprint, tag


class Body(BaseModel):
    street: str
    price: int
    plan: str


@blueprint.post("", tags=[tag])
def post_property(body: Body):
    try:
        with DatabaseSession() as s:
            statement = select(Address).where(Address.street == body.street)
            address = s.scalars(statement).first()

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
                address = s.scalars(statement).first()

            property = Property(
                address_id=address.id,
                price=body.price,
                plan=body.plan,
                photo="template_house_0.svg",
            )

            s.add(property)
            s.commit()

        return ("Adicionado", 200)
    except Exception as e:
        print(e)
        return ("Error", 500)
