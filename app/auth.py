import functools

from flask_openapi3 import APIBlueprint, Tag
from flask import g, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from app.database import get_db

blueprint = APIBlueprint("auth", __name__, url_prefix="/auth")

register_tag = Tag(name="Autenticação", description="Registra uma nova conta")
login_tag = Tag(name="Autenticação", description="Acessa uma conta")
logout_tag = Tag(name="Autenticação", description="Sai da conta atual")


@blueprint.post("/register", tags=[register_tag])
def register():
    email = request.form["email"]
    password = request.form["password"]
    database = get_db()

    if not email:
        return ("Email não providênciado", 400)

    if not password:
        return ("Senha não providênciada", 400)

    try:
        database.execute(
            "INSERT INTO accounts (email, password) VALUES (?, ?)",
            (email, generate_password_hash(password)),
        )
        database.commit()
    except database.IntegrityError:
        return ("Email já havia sido registrado", 400)

    return ("Criado", 201)


@blueprint.post("/login", tags=[login_tag])
def login():
    email = request.form["email"]
    password = request.form["password"]
    database = get_db()

    account = database.execute(
        "SELECT * FROM accounts where email = ?", (email,)
    ).fetchone()

    if account is None:
        return ("Email incorreto", 400)

    if not check_password_hash(account["password"], password):
        return ("Senha incorreta", 400)

    session.clear()
    session["account_id"] = account["id"]

    return ("Acesso concedido", 200)


@blueprint.before_app_request
def load_logged_in_user():
    g.account = session.get("account_id")

    if not g.account:
        return

    g.account = (
        get_db().execute("SELECT * FROM accounts WHERE id = ?", (g.account,)).fetchone()
    )


@blueprint.route("/logout")
def logout(tags=[logout_tag]):
    session.clear()
    return ("Acesso revogado", 200)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.account is None:
            return ("Não autorizado", 401)
        return view(**kwargs)

    return wrapped_view
