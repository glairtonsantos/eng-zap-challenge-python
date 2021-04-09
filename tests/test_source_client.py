import os
import requests
from unittest import TestCase, mock
from dotenv import load_dotenv
from eng_zap_challenge_python.client import source_client, try_connection

URL_WRONG = (
    "http://grupozap-code-challenge.s3-website-us-east-111.amazonaws.com/"
)
URL_NOT_FOUND = (
    "http://grupozap-code-challenge.s3-website-us-east-1.amazonaws.com/"
    "sources404/source-2.json"
)


class SourceClientTest(TestCase):
    def setUp(self):
        self.client = source_client

    def test_connection_error(self):
        @try_connection
        def method_decorated():
            r = requests.get(URL_WRONG)
            return r.text, r.status_code

        self.assertRaises(Exception, method_decorated)

    def test_get_source_success(self):
        load_dotenv()
        self.client.load_data_source()

        self.assertIsInstance(self.client.data_source, list)

    @mock.patch.dict(os.environ, {"URL_SOURCE": URL_NOT_FOUND})
    def test_get_source_error(self):
        load_dotenv()

        self.assertRaises(Exception, self.client.load_data_source)

    @mock.patch.dict(os.environ, {"URL_SOURCE": ""})
    def test_get_source_without_url(self):
        load_dotenv()

        self.assertRaises(Exception, self.client.load_data_source)
