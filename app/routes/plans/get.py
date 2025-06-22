from sqlalchemy import select

from app.database import DatabaseSession
from app.database.plans import Plan
from app.routes.plans import blueprint, tag


@blueprint.get("", tags=[tag])
def get_property():
    try:
        with DatabaseSession() as s:
            plans = select(Plan)
            plans = s.scalars(plans).all()
            plans = [p.dict() for p in plans]

            return plans
    except Exception as exception:
        print(f"{exception=}")
        return ("Error", 500)

    return ("Imóvel não encontrado", 404)
