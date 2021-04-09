import requests
import logging
from flask_api import status
from requests.exceptions import ConnectionError
from . import URL_SOURCE


def try_connection(access):
    def wrapper(*args, **kwargs):
        try:
            return access(*args, **kwargs)
        except ConnectionError as err:
            raise Exception(
                f"error in conection with {err.request.url} detail: {str(err)}"
            )

    return wrapper


class SourceClient:
    data_source = []

    @try_connection
    def load_data_source(self, url_source=URL_SOURCE):

        if url_source:

            logging.warning(f"wait...load source from {url_source}")
            r = requests.get(url_source)

            if r.status_code != status.HTTP_200_OK:
                raise Exception(
                    (
                        "Fail in load data source"
                        f"status:{r.status_code} - {r.text}"
                    )
                )

            self.data_source = r.json()
        else:
            raise Exception("URL_SOURCE is not defined")


source_client = SourceClient()
