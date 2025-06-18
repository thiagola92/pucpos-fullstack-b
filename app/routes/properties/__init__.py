from flask_openapi3 import APIBlueprint

from app.routes.property import tag as t


blueprint = APIBlueprint("properties", __name__, url_prefix="/properties")
tag = t
