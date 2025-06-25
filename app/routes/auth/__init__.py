import functools

import jwt
from datetime import datetime, UTC
from flask import g, session, request
from flask_openapi3 import APIBlueprint, Tag
from sqlalchemy import select

from app.secret import SECRET_KEY
from app.database import DatabaseSession
from app.database.accounts import Account


blueprint = APIBlueprint("auth", __name__, url_prefix="/auth")
tag = Tag(name="Autenticação", description="Gerencia o acesso do usuário à página web")


@blueprint.before_app_request
def load_logged_in_user():
    g.account = None

    encoded = session.get("token") or request.headers.get("token")

    if not encoded:
        return

    try:
        token = jwt.decode(encoded, SECRET_KEY, algorithms="HS256")
    except Exception as e:
        print(f'Fail to decode: "{encoded}"\nError: {e}')
        return

    if "expiration" not in token:
        return

    if token["expiration"] < datetime.now(UTC).timestamp():
        return

    g.account = token["account_id"]

    if not g.account:
        return

    with DatabaseSession() as s:
        statement = select(Account).where(Account.id == g.account).limit(1)
        g.account = s.scalar(statement).id


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.account is None:
            return ("Não autorizado", 401)
        return view(**kwargs)

    return wrapped_view
