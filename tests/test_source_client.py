import os
import requests
from flask_api import status
from unittest import TestCase, mock
from dotenv import load_dotenv
from eng_zap_challenge_python.client import SourceClient, try_connection

URL_WRONG = "http://grupozap-code-challenge.s3-website-us-east-111.amazonaws.com/"
URL_NOT_FOUND = "http://grupozap-code-challenge.s3-website-us-east-1.amazonaws.com/sources404/source-2.json"


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
        self.assertEqual(
            content.get("message"), (f"error in conection with {URL_WRONG}")
        )

    def test_get_source_success(self):
        load_dotenv()

        res, status_code = self.client.get_source()

        self.assertTrue(status_code == status.HTTP_200_OK)
        self.assertIsInstance(res, list)

    @mock.patch.dict(os.environ, {"URL_SOURCE": URL_NOT_FOUND})
    def test_get_source_error(self):
        load_dotenv()
        res, status_code = self.client.get_source()

        self.assertTrue(status_code != status.HTTP_200_OK)
        self.assertIsInstance(res, str)
