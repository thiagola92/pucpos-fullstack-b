import jwt
from datetime import datetime, UTC, timedelta
from werkzeug.security import check_password_hash
from sqlalchemy import select
from pydantic import BaseModel, EmailStr

from app.secret import SECRET_KEY
from app.routes.auth import blueprint, tag
from app.database import DatabaseSession
from app.database.accounts import Account


class AuthLoginPost(BaseModel):
    email: EmailStr
    password: str


@blueprint.post("/login", tags=[tag])
def login(form: AuthLoginPost):
    with DatabaseSession() as s:
        statement = select(Account).where(Account.email == form.email).limit(1)
        account = s.scalar(statement)

        if account is None:
            return ("Email incorreto", 400)

        if not check_password_hash(account.password, form.password):
            return ("Senha incorreta", 400)

    expiration = datetime.now(UTC) + timedelta(1)
    encoded = jwt.encode(
        {"account_id": str(account.id), "expiration": expiration.timestamp()},
        SECRET_KEY,
        algorithm="HS256",
    )

    return (encoded, 200)
