from sqlalchemy import select

from app.database import DatabaseSession
from app.database.plans import Plan
from app.routes.plans import blueprint, tag


description = "Obtém todos os planos para os imóveis (vender, alugar, etc) suportados pela plataforma."


responses = {
    200: {
        "content": {
            "application/json": {
                "schema": {
                    "type": "array",
                    "example": '[{"id": 1, "action": "Vender"}]',
                },
            }
        }
    }
}


@blueprint.get("", tags=[tag], description=description, responses=responses)
def get_plan():
    with DatabaseSession() as s:
        plans = select(Plan)
        plans = s.scalars(plans).all()
        plans = [p.dict() for p in plans]

        return plans
