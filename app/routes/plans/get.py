from sqlalchemy import select

from app.database import DatabaseSession
from app.database.plans import Plan
from app.routes.plans import blueprint, tag


@blueprint.get("", tags=[tag])
def get_plan():
    with DatabaseSession() as s:
        plans = select(Plan)
        plans = s.scalars(plans).all()
        plans = [p.dict() for p in plans]

        return plans
