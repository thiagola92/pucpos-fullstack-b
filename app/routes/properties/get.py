from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional

from app.database import DatabaseSession
from app.database.properties import Property
from app.database.addresses import Address
from app.routes.properties import blueprint, tag


class Query(BaseModel):
    street: str = ""


@blueprint.get("", tags=[tag])
def get_properties(query: Query):
    try:
        with DatabaseSession() as s:
            query.street = f"%{query.street}%"

            addr_statement = select(Address).where(Address.street.like(query.street))
            addr_rows = {r.id: r.dict() for r in s.scalars(addr_statement).all()}

            prop_statement = select(Property).where(
                Property.address_id.in_(addr_rows.keys())
            )
            prop_rows = s.scalars(prop_statement).all()

            results = [r.dict() for r in prop_rows]

            for r in results:
                r["address"] = addr_rows[r["address_id"]]

            return results
    except Exception as e:
        print(e)

    return ("Error", 500)
