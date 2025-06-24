from pydantic import BaseModel, Field
from sqlalchemy import select

from app.database import DatabaseSession
from app.database.properties import Property
from app.routes.property import blueprint, tag
from app.routes.generic import generic404


class PropertyResponse(BaseModel):
    id: int
    address_id: int
    price: int
    plan_id: int
    type_id: int
    photo: str


description = "Pega informações de um imóvel."

responses = {
    404: generic404,
    200: PropertyResponse,
}


class PropertyGet(BaseModel):
    id: int = Field(description="O identificador do imóvel.")


@blueprint.get("<int:id>", tags=[tag], description=description, responses=responses)
def get_property(path: PropertyGet):
    statement = select(Property).where(Property.id == path.id)

    with DatabaseSession() as s:
        row = s.scalars(statement).first()

        if row:
            return row.dict()

    return ("Não encontrado", 404)
