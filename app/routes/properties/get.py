from sqlalchemy import select, or_
from pydantic import BaseModel
from flask import g

from app.database import DatabaseSession
from app.database.properties import Property
from app.database.addresses import Address
from app.database.plans import Plan
from app.database.types import Type
from app.database.property_owners import PropertyOwner
from app.routes.properties import blueprint, tag, security_r
from app.routes.auth import load_logged_in_user


class Query(BaseModel):
    plan: int = 3
    type: int = 3
    street: str = ""
    account_id: int = -1


@blueprint.get("", tags=[tag], security=security_r)
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

    if id == 0 and "account" in g:
        id = g.account
    print(id)

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
