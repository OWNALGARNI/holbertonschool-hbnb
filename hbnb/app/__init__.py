from flask import Flask
from app.api import init_api


def create_app():
    app = Flask(__name__)
    app.config["RESTX_MASK_SWAGGER"] = False

    init_api(app)

    return app
