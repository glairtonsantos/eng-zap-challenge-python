from flask import request
from flask_api import status
from . import app
from .filters import SourceFilter
from .client import source_client
from .pagination import SourcePagination


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


@app.route("/properties/<context>/", methods=["GET"])
def source(context):
    source_filter = SourceFilter(context.lower(), source_client.data_source)
    filtered = source_filter.filter()
    paginator = SourcePagination(request.args, filtered)

    return (paginator.response(), status.HTTP_200_OK)
