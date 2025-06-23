from flask_openapi3 import APIBlueprint, Tag


blueprint = APIBlueprint("type", __name__, url_prefix="/type")
tag = Tag(name="Types", description="")
