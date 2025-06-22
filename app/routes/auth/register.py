from flask import request
from werkzeug.security import generate_password_hash
from pydantic import BaseModel, EmailStr

from app.routes.auth import blueprint, tag
from app.database import DatabaseSession
from app.database.accounts import Account


class RegistrationForm(BaseModel):
    email: EmailStr
    password: str
    name: str
    cpf: str
    phone: str


@blueprint.post("/register", tags=[tag])
def register(form: RegistrationForm):
    try:
        with DatabaseSession() as s:
            account = Account(
                email=form.email,
                password=generate_password_hash(form.password),
            )
            s.add(account)
            s.commit()
    except Exception as exception:
        print(f"{exception=}")
        return ("Error", 500)

    return ("Criado", 201)
