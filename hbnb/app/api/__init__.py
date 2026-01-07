from flask_restx import Api
from app.api.v1 import namespaces

api = Api(
    title="HBnB API",
    version="1.0",
    description="HBnB application API",
    doc="/docs",
)

def init_api(app):
    api.init_app(app)

    # Force /api/v1/<namespace_name> as base path
    for ns in namespaces:
        api.add_namespace(ns, path=f"/api/v1/{ns.name}")
