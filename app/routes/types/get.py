from sqlalchemy import select

from app.database import DatabaseSession
from app.database.types import Type
from app.routes.types import blueprint, tag


description = "Obtém todos os tipos de imóveis (casa, apartamento, etc) suportados pela plataforma."


responses = {
    200: {
        "content": {
            "application/json": {
                "schema": {
                    "type": "array",
                    "example": '[{"id": 1, "name": "Casa"}]',
                },
            }
        }
    }
}


@blueprint.get("", tags=[tag], description=description, responses=responses)
def get_types():
    with DatabaseSession() as s:
        types = select(Type)
        types = s.scalars(types).all()
        types = [p.dict() for p in types]

        return types
