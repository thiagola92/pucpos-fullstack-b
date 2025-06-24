from flask_openapi3 import APIBlueprint, Tag


blueprint = APIBlueprint("plans", __name__, url_prefix="/plans")
tag = Tag(name="Planos", description="")
