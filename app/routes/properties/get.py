from sqlalchemy import select
from pydantic import BaseModel
from flask import g

from app.database import DatabaseSession
from app.database.properties import Property
from app.database.addresses import Address
from app.database.property_owners import PropertyOwner
from app.routes.properties import blueprint, tag
from app.routes.auth import load_logged_in_user


class Query(BaseModel):
    street: str = ""
    account_id: int = -1


@blueprint.get("", tags=[tag])
def get_properties(query: Query):
    try:
        if query.account_id > -1:
            return query_by_id(query.account_id)
        else:
            return query_by_street(query.street)
    except Exception as exception:
        print(f"{exception=}")
        return ("Error", 500)


def query_by_street(street: str):
    with DatabaseSession() as s:
        street = f"%{street}%"

        address_statement = select(Address).where(Address.street.like(street))
        addresses = {r.id: r.dict() for r in s.scalars(address_statement).all()}

        property_statement = select(Property).where(
            Property.address_id.in_(addresses.keys())
        )
        properties = s.scalars(property_statement).all()
        properties = [r.dict() for r in properties]

        for p in properties:
            p["address"] = addresses[p["address_id"]]

        return properties


def query_by_id(id: str):
    load_logged_in_user()

    if id == 0 and "account" in g:
        id = g.account

    with DatabaseSession() as s:
        owned = select(PropertyOwner).where(PropertyOwner.account_id == id)
        owned = [r.property_id for r in s.scalars(owned).all()]

        addresses = select(Address).where(Address.id.in_(owned))
        addresses = {r.id: r.dict() for r in s.scalars(addresses).all()}

        properties = select(Property).where(Property.id.in_(owned))
        properties = s.scalars(properties).all()
        properties = [r.dict() for r in properties]

        for p in properties:
            p["address"] = addresses[p["address_id"]]

        return properties
