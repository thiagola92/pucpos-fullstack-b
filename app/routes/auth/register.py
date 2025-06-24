from werkzeug.security import generate_password_hash
from pydantic import BaseModel, EmailStr, ConfigDict

from app.routes.auth import blueprint, tag
from app.database import DatabaseSession
from app.database.accounts import Account
from app.routes.generic import generic201


responses = {201: generic201}


class AuthRegisterPost(BaseModel):
    email: EmailStr
    password: str
    name: str
    cpf: str
    phone: str

    model_config = ConfigDict(coerce_numbers_to_str=True)


@blueprint.post("/register", tags=[tag], responses=responses)
def register(form: AuthRegisterPost):
    with DatabaseSession() as s:
        account = Account(
            email=form.email,
            password=generate_password_hash(form.password),
        )
        s.add(account)
        s.commit()

    return ("Criado", 201)
