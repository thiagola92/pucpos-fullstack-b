from flask_openapi3 import APIBlueprint, Tag


security_w = [{"api_key": ["write:property"]}]
blueprint = APIBlueprint("property", __name__, url_prefix="/property")
tag = Tag(name="Imóvel", description="Operações sobre imóveis")
