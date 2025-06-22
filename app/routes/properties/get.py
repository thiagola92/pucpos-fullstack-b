from sqlalchemy import select
from pydantic import BaseModel
from flask import g, session

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
    except Exception as e:
        print(e)

    return ("Error", 500)


def query_by_street(street: str):
    # TODO: use JOIN
    with DatabaseSession() as s:
        street = f"%{street}%"

        addr_statement = select(Address).where(Address.street.like(street))
        addr_rows = {r.id: r.dict() for r in s.scalars(addr_statement).all()}

        prop_statement = select(Property).where(
            Property.address_id.in_(addr_rows.keys())
        )
        prop_rows = s.scalars(prop_statement).all()

        results = [r.dict() for r in prop_rows]

        for r in results:
            r["address"] = addr_rows[r["address_id"]]

        return results


def query_by_id(id: str):
    load_logged_in_user()

    if id == 0 and "account" in g:
        id = g.account

    # TODO: use JOIN
    with DatabaseSession() as s:
        owner_statement = select(PropertyOwner).where(PropertyOwner.account_id == id)
        prop_ids = [r.property_id for r in s.scalars(owner_statement).all()]

        addr_statement = select(Address).where(Address.id.in_(prop_ids))
        addr_rows = {r.id: r.dict() for r in s.scalars(addr_statement).all()}

        prop_statement = select(Property).where(
            Property.address_id.in_(addr_rows.keys())
        )
        prop_rows = s.scalars(prop_statement).all()

        results = [r.dict() for r in prop_rows]

        for r in results:
            r["address"] = addr_rows[r["address_id"]]

        return results
