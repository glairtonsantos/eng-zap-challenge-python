from flask import request
from . import app
from .filters import SourceFilter
from .client import source_client

# from .client import data_response


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


def paginate(result, page_size):
    return [result[i : i + page_size] for i in range(0, len(result), page_size)]


@app.route("/properties/<context>/", methods=["GET"])
def source(context):
    source_filter = SourceFilter(context.lower(), source_client.data_source)
    filtered = source_filter.filter()

    page = request.args.get("page", 1)
    page_size = request.args.get("page_size", 10)
    paginated = paginate(filtered, int(page_size))[int(page) - 1] if filtered else []

    response_data = {
        "pageNumber": page,
        "pageSize": len(paginated),
        "totalCount": len(filtered),
        "listings": paginated,
    }

    return (response_data, 200)
