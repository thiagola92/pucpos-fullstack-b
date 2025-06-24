from flask_openapi3 import APIBlueprint, Tag


blueprint = APIBlueprint("plan", __name__, url_prefix="/plan")
tag = Tag(name="Plano", description="")
