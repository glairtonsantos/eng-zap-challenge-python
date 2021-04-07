import os
import requests
from flask_api import status
from requests.exceptions import ConnectionError


def try_connection(access):
    def wrapper(*args, **kwargs):
        try:
            return access(*args, **kwargs)
        except ConnectionError as err:
            return (
                {
                    "message": f"error in conection with {err.request.url}",
                    "erro_detail": str(err),
                },
                status.HTTP_503_SERVICE_UNAVAILABLE,
            )

    return wrapper


class SourceClient:
    @try_connection
    def get_source(self):
        URL_SOURCE = os.environ.get("URL_SOURCE")
        r = requests.get(URL_SOURCE)
        if r.status_code != status.HTTP_200_OK:
            return r.text, r.status_code

        content = r.json()

        return content, status.HTTP_200_OK
