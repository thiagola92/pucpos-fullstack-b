from app.logger import logger

from werkzeug.security import generate_password_hash
from pydantic import BaseModel, EmailStr, ConfigDict, Field
from sqlalchemy.exc import IntegrityError

from app.routes.auth import blueprint, tag
from app.database import DatabaseSession
from app.database.accounts import Account
from app.routes.util import generic_message


responses = {201: {}, 400: generic_message(), 500: {}}


class AuthRegisterPost(BaseModel):
    email: EmailStr = "asdf@asdf.com"
    password: str = "asdf"
    name: str = "ASDF"
    cpf: str = Field("123.456.789-05")
    phone: str = Field("999999999")

    model_config = ConfigDict(coerce_numbers_to_str=True)


@blueprint.post("/register", tags=[tag], responses=responses)
def register(form: AuthRegisterPost):
    try:
        with DatabaseSession() as s:
            account = Account(
                email=form.email,
                password=generate_password_hash(form.password),
            )

            s.add(account)
            s.commit()

        return ("", 201)
    except IntegrityError as e:
        logger.error(e)
        return ("Um dos seguintes campos já existe no banco: email, phone", 400)
    except Exception as e:
        logger.error(e)
        return ("", 500)
