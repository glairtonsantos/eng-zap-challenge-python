from flask import jsonify
from . import app

@app.route("/")
def about():
    description = {
        "name": "Code Challenge Grupo ZAP",
        "version": "0.0.1",
        "about":"separate properties eligible for ZAP or pro Viva Real according to the proposed rules",
        "license": "MIT"
    }
    return jsonify(description)