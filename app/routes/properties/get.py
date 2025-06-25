from sqlalchemy import select, or_
from pydantic import BaseModel, Field
from flask import g

from app.database import DatabaseSession
from app.database.properties import Property
from app.database.addresses import Address
from app.database.plans import Plan
from app.database.types import Type
from app.database.property_owners import PropertyOwner
from app.routes.properties import blueprint, tag, security_r
from app.routes.auth import load_logged_in_user


description = "Busca imóveis."

responses = {
    200: {
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "example": """[{
                        "address": {
                            "city": "Rio de Janeiro",
                            "country": "Brasil",
                            "extra": "",
                            "house_number": 20,
                            "id": 1,
                            "state": "RJ",
                            "street": "Av. Padre Leonel Franca"
                        },
                        "address_id": 1,
                        "id": 1,
                        "photo": "template_house_0.svg",
                        "plan": {
                            "action": "Vender",
                            "id": 1
                        },
                        "plan_id": 1,
                        "price": 100000000,
                        "type": {
                            "id": 1,
                            "name": "Casa"
                        },
                        "type_id": 1
                    }]""",
                },
            }
        }
    }
}

plan_description = """[Bit field](https://en.wikipedia.org/wiki/Bit_field) para indicar os planos dos imóveis os quais está buscando.  
1 - Imóveis à venda  
2 - Imóveis para alugar  
---  
"""

type_description = """[Bit field](https://en.wikipedia.org/wiki/Bit_field) para indicar os tipos de imóveis os quais está buscando.  
1 - Casa  
2 - Apartamento  
---  
"""

account_description = """O Identificador da conta o qual deseja ver os imóveis.  
**3** - Imóveis da conta com identificador 3  
**2** - Imóveis da conta com identificador 2  
**1** - Imóveis da conta com identificador 1  
**0** - Imóveis da sua conta (requer estar autenticado)  
**-1** - Imóveis de todas as contas  
---  
"""


class Query(BaseModel):
    plan: int = Field(3, description=plan_description)
    type: int = Field(3, description=type_description)
    street: str = Field("", description="A rua do imóvel")
    account_id: int = Field(-1, description=account_description)


@blueprint.get(
    "", tags=[tag], description=description, responses=responses, security=security_r
)
def get_properties(query: Query):
    if query.account_id > -1:
        return query_by_id(query.account_id)
    else:
        return query_by_street(query)


def query_by_street(query: Query):
    with DatabaseSession() as s:
        street = f"%{query.street}%"

        addresses = select(Address).where(Address.street.like(street))
        addresses = {r.id: r.dict() for r in s.scalars(addresses).all()}

        plans = select(Plan)
        plans = s.scalars(plans).all()
        plans = {t.id: t.dict() for t in plans}

        types = select(Type)
        types = s.scalars(types).all()
        types = {p.id: p.dict() for p in types}

        properties = select(Property).where(Property.address_id.in_(addresses.keys()))

        if query.plan == 3:
            properties = properties.where(
                or_(Property.plan_id == 1, Property.plan_id == 2)
            )
        elif query.plan == 2:
            properties = properties.where(Property.plan_id == 2)
        elif query.plan == 1:
            properties = properties.where(Property.plan_id == 1)

        if query.type == 3:
            properties = properties.where(
                or_(Property.type_id == 1, Property.type_id == 2)
            )
        elif query.type == 2:
            properties = properties.where(Property.type_id == 2)
        elif query.type == 1:
            properties = properties.where(Property.type_id == 1)

        properties = s.scalars(properties).all()
        properties = [r.dict() for r in properties]

        for p in properties:
            p["address"] = addresses[p["address_id"]]
            p["plan"] = plans[p["plan_id"]]
            p["type"] = types[p["type_id"]]

        return properties


def query_by_id(id: str):
    load_logged_in_user()

    if id == 0 and g.account:
        id = g.account

    with DatabaseSession() as s:
        owned = select(PropertyOwner).where(PropertyOwner.account_id == id)
        owned = [r.property_id for r in s.scalars(owned).all()]

        properties = select(Property).where(Property.id.in_(owned))
        properties = s.scalars(properties).all()
        properties = [r.dict() for r in properties]

        addresses = [p["address_id"] for p in properties]
        addresses = select(Address).where(Address.id.in_(addresses))
        addresses = {r.id: r.dict() for r in s.scalars(addresses).all()}

        plans = select(Plan)
        plans = s.scalars(plans).all()
        plans = {p.id: p.dict() for p in plans}

        types = select(Plan)
        types = s.scalars(types).all()
        types = {p.id: p.dict() for p in types}

        for p in properties:
            p["address"] = addresses[p["address_id"]]
            p["plan"] = plans[p["plan_id"]]
            p["type"] = plans[p["type_id"]]

        return properties
