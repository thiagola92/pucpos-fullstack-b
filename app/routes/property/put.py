from pydantic import BaseModel, Field
from flask import g
from sqlalchemy import select

from app.database import DatabaseSession
from app.database.properties import Property
from app.database.addresses import Address
from app.routes.property import blueprint, tag, security_w
from app.routes.auth import login_required
from app.routes.generic import generic200, generic401, generic404


description = "Cria um imóvel."

responses = {
    200: generic200,
    401: generic401,
    404: generic404,
}


class PropertyPut(BaseModel):
    id: int = Field(description="O identificador do imóvel.")
    street: str = Field(description="A rua do imóvel.")
    price: int | float = Field(1, description="O preço do imóvel (mínimo de 1 real).")
    plan_id: int = Field(description="O identificador do plano do imóvel.")
    type_id: int = Field(description="O identificador do tipo de imóvel.")


@blueprint.put(
    "", tags=[tag], description=description, responses=responses, security=security_w
)
@login_required
def put_property(body: PropertyPut):
    with DatabaseSession() as s:
        property = select(Property).where(Property.id == body.id)
        property = s.scalars(property).first()

        if not property:
            return ("Não encontrado", 404)

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

    return ("Sucesso", 200)
