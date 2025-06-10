from flask_openapi3 import Tag
from flask import request
from werkzeug.security import generate_password_hash

from app.routes.auth import blueprint, tag
from app.database import DatabaseSession
from app.database.accounts import Account


@blueprint.post("/register", tags=[tag])
def register():
    email = request.form["email"]
    password = request.form["password"]

    if not email:
        return ("Email não providênciado", 400)

    if not password:
        return ("Senha não providênciada", 400)

    try:
        with DatabaseSession() as s:
            account = Account(email=email, password=generate_password_hash(password))
            s.add(account)
            s.commit()
    except Exception as e:
        print(e)  # Remover no futuro.
        return ("Error ao registar", 500)

    return ("Criado", 201)
