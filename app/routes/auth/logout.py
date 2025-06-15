from flask import session

from app.routes.auth import blueprint, tag


@blueprint.post("/logout", tags=[tag])
def logout():
    session.clear()
    return ("Acesso revogado", 200)
