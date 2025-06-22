import os
from pathlib import Path

from flask import redirect
from flask_cors import CORS
from flask_openapi3 import OpenAPI, Info

from app.secret import SECRET_KEY
from app.routes import auth, property, properties, plans
from app.database import init_db_command, close_db


info = Info(title="House API", version="1.0.0")
app = OpenAPI(__name__, info=info, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY=SECRET_KEY,
    DATABASE=Path(app.instance_path).joinpath("app.sqlite"),
)

CORS(app, supports_credentials=True)
os.makedirs(app.instance_path, exist_ok=True)

app.cli.add_command(init_db_command)
app.teardown_appcontext(close_db)
app.register_api(auth.blueprint)
app.register_api(property.blueprint)
app.register_api(properties.blueprint)
app.register_api(plans.blueprint)


@app.route("/")
def index():
    return redirect("/openapi")
