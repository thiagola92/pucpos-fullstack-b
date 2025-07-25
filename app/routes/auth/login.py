from app.logger import logger

import jwt
from datetime import datetime, UTC, timedelta
from werkzeug.security import check_password_hash
from sqlalchemy import select
from pydantic import BaseModel, EmailStr, ConfigDict

from app.secret import SECRET_KEY
from app.routes.auth import blueprint, tag
from app.database import DatabaseSession
from app.database.accounts import Account
from app.routes.util import generic_message


responses = {
    200: {
        "content": {
            "text/plain": {
                "schema": {
                    "type": "string",
                    "example": "eyJhbGciOiJIUzI1N4IsInR5cCI6IkpXVCJ9.eyJhY2NvdW53X2lkIjoiMSIsImV4cGlyYXRpb24iOjE3NTA4MjIwMTQuNDQ0MDQxfQ.5m821-DNq6Fzi4jnmjJLveYcn63OPcWGuG7pdCKksC4",
                }
            }
        },
        "description": "O token a ser utilizado na autênticação.",
    },
    400: generic_message(),
    500: {},
}


class AuthLoginPost(BaseModel):
    email: EmailStr = "asdf@asdf.com"
    password: str = "asdf"

    model_config = ConfigDict(coerce_numbers_to_str=True)


@blueprint.post("/login", tags=[tag], responses=responses)
def login(form: AuthLoginPost):
    try:
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
    except Exception as e:
        logger.error(e)
        return ("", 500)
