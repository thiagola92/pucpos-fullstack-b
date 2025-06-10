from flask_openapi3 import Tag
from flask import request, session
from werkzeug.security import check_password_hash
from sqlalchemy import select

from app.routes.auth import blueprint, tag
from app.database import DatabaseSession
from app.database.accounts import Account


@blueprint.post("/login", tags=[tag])
def login():
    email = request.form["email"]
    password = request.form["password"]

    with DatabaseSession() as s:
        statement = select(Account).where(Account.email == email).limit(1)
        account = s.scalar(statement)

        if account is None:
            return ("Email incorreto", 400)

        if not check_password_hash(account.password, password):
            return ("Senha incorreta", 400)

    session.clear()
    session["account_id"] = account["id"]

    return ("Acesso concedido", 200)
