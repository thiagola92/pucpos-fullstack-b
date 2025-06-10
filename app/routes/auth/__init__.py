import functools

from flask import g, session
from flask_openapi3 import APIBlueprint, Tag
from sqlalchemy import select

from app.database import DatabaseSession
from app.database.accounts import Account


blueprint = APIBlueprint("auth", __name__, url_prefix="/auth")
tag = Tag(name="Autenticação", description="Gerencia o acesso do usuário à página web")


@blueprint.before_app_request
def load_logged_in_user():
    g.account = session.get("account_id")

    if not g.account:
        return

    with DatabaseSession as s:
        statement = select(Account).where(Account.id == g.account).limit(1)
        g.account = s.scalar(statement)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.account is None:
            return ("Não autorizado", 401)
        return view(**kwargs)

    return wrapped_view
