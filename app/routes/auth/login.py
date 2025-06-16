import jwt
from werkzeug.security import check_password_hash
from sqlalchemy import select
from pydantic import BaseModel, EmailStr

from app.secret import SECRET_KEY
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

    encoded = jwt.encode(
        {"account_id": str(account.id)},
        SECRET_KEY,
        algorithm="HS256",
    )

    return (encoded, 200)
