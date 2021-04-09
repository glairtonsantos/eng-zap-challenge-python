from flask import Blueprint
from flask_api import FlaskAPI

URL_SOURCE = "http://grupozap-code-challenge.s3-website-us-east-1.amazonaws.com/sources/source-2.json"

blueprint = Blueprint("eng_zap_challenge_python", __name__)


def create_app(config="dev"):
    app = FlaskAPI(__name__)

    app.register_blueprint(blueprint)

    return app


from . import views