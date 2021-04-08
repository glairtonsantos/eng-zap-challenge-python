import os
import requests
import logging
from flask_api import status
from requests.exceptions import ConnectionError


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
    def load_data_source(self):
        URL_SOURCE = os.environ.get("URL_SOURCE")

        if URL_SOURCE:

            logging.warning(f"wait...load source from {URL_SOURCE}")
            r = requests.get(URL_SOURCE)

            if r.status_code != status.HTTP_200_OK:
                raise Exception(
                    f"Fail in load data source: status:{r.status_code} - {r.text}"
                )

            self.data_source = r.json()
        else:
            raise Exception("URL_SOURCE is not defined in env")


source_client = SourceClient()
