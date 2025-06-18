from flask_openapi3 import APIBlueprint, Tag


blueprint = APIBlueprint("property", __name__, url_prefix="/property")
tag = Tag(name="Imóvel", description="Operações sobre um único imóvel")
