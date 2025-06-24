from flask_openapi3 import APIBlueprint

from app.routes.property import tag as t


security_r = [{"api_key": ["read:properties"]}]
blueprint = APIBlueprint("properties", __name__, url_prefix="/properties")
tag = t
