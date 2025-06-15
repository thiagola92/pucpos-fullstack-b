from flask import session
from werkzeug.security import check_password_hash
from sqlalchemy import select
from pydantic import BaseModel, EmailStr

from app.routes.auth import blueprint, tag
from app.database import DatabaseSession
from app.database.accounts import Account


class LoginForm(BaseModel):
    email: EmailStr
    password: str


@blueprint.post("/login", tags=[tag])
def login(form: LoginForm):
    with DatabaseSession() as s:
        statement = select(Account).where(Account.email == form.email).limit(1)
        account = s.scalar(statement)

        if account is None:
            return ("Email incorreto", 400)

        if not check_password_hash(account.password, form.password):
            return ("Senha incorreta", 400)

    session.clear()
    session["account_id"] = account["id"]

    return ("Acesso concedido", 200)
