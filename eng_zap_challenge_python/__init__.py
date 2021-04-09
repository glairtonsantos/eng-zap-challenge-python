from flask import Blueprint
from flask_api import FlaskAPI

blueprint = Blueprint("eng_zap_challenge_python", __name__)


def create_app(config="dev"):
    app = FlaskAPI(__name__)

    app.register_blueprint(blueprint)

    return app


from . import views