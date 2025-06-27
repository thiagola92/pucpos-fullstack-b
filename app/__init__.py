import os
from pathlib import Path

from flask import redirect
from flask_cors import CORS
from flask_openapi3 import OpenAPI, Info, Tag

from app.secret import SECRET_KEY
from app.routes import auth, property, properties
from app.database import init_db_command, close_db


info = Info(title="House API", version="1.0.0")
security_schemes = {
    "api_key": {
        "type": "apiKey",
        "name": "token",
        "in": "header",
    }
}
app = OpenAPI(
    __name__,
    info=info,
    instance_relative_config=True,
    security_schemes=security_schemes,
)
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

tag = Tag(name="Documentação", description="Documentação Swagger")


@app.get("/", tags=[tag])
def index():
    return redirect("/openapi/swagger")
