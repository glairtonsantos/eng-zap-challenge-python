from . import app
from .client import SourceClient


@app.route("/")
def about():
    return {
        "name": "Code Challenge Grupo ZAP",
        "version": "0.0.1",
        "about": (
            "separate properties eligible for ZAP or "
            "Viva Real according to the proposed rules"
        ),
        "license": "MIT",
    }


@app.route("/source/")
def source():
    client = SourceClient()

    res, status = client.get_source()

    return {"content": res}, status
