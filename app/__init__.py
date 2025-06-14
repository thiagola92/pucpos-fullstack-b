import os
from pathlib import Path

from flask import redirect
from flask_cors import CORS
from flask_openapi3 import OpenAPI, Info

from app.routes import auth
from app.database import init_db_command, close_db

# Não se deve botar segredos hardcoded,
# mas o foco não é segurança neste trabalho.
SECRET_KEY = "227067b319a17f73cb49cad9c61f6b7a7dd9aa7852035e406a5ea86bb3a2d486"


def create_app(test_config=None):
    info = Info(title="House API", version="1.0.0")
    app = OpenAPI(__name__, info=info, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=SECRET_KEY,
        DATABASE=Path(app.instance_path).joinpath("app.sqlite"),
    )

    CORS(app)

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.cli.add_command(init_db_command)
    app.teardown_appcontext(close_db)
    app.register_api(auth.blueprint)

    @app.route("/")
    def index():
        return redirect("/openapi")

    return app
