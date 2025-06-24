from flask_openapi3 import APIBlueprint, Tag


blueprint = APIBlueprint("types", __name__, url_prefix="/types")
tag = Tag(name="Types", description="")
