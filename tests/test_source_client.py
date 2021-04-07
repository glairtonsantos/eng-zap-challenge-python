import requests
from flask_api import status
from unittest import TestCase
from eng_zap_challenge_python.client import SourceClient, try_connection

URL_WRONG = "http://grupozap-code-challenge.s3-website-us-east-111.amazonaws.com/"


class TestSourceClient(TestCase):
    def setUp(self):
        self.client = SourceClient()

    def test_connection_error(self):
        @try_connection
        def method_decorated():
            r = requests.get(URL_WRONG)
            return r.text, r.status_code

        content, status_code = method_decorated()

        self.assertEqual(status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertEqual(content.get("message"), f"error in conection with {URL_WRONG}")
