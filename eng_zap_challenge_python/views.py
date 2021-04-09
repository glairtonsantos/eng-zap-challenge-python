from flask import request
from . import blueprint
from .filters import SourceFilter
from .client import source_client
from .pagination import SourcePagination


@blueprint.route("/")
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


@blueprint.route("/properties/<context>/", methods=["GET"])
def source(context):

    source_filter = SourceFilter(context.lower(), source_client.data_source)
    filtered = source_filter.filter()
    paginator = SourcePagination(request.args, filtered)

    return paginator.response()
