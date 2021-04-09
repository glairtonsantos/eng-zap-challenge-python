import os
from unittest import TestCase, mock
from dotenv import load_dotenv
from flask_api import status
from eng_zap_challenge_python.client import source_client
from eng_zap_challenge_python import create_app

URL_SOURCE = "http://grupozap-code-challenge.s3-website-us-east-1.amazonaws.com/sources/source-1.json"


class SourceListTest(TestCase):
    @mock.patch.dict(os.environ, {"URL_SOURCE": URL_SOURCE})
    def setUp(self):
        load_dotenv()
        source_client.load_data_source()

        self.app = create_app(config="test")
        self.client = self.app.test_client()

        self.headers = {'content-type': 'application/json'}

    def test_list_source(self):
        response = self.client.get(
            "/properties/zap/",
            content_type="application/json",
            headers=self.headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.get_json()['listings']), 50)
        self.assertEqual(response.get_json()['pageNumber'], 1)
        self.assertEqual(response.get_json()['pageSize'], 50)
        self.assertEqual(response.get_json()['totalCount'], 73)

        response = self.client.get(
            "/properties/zap/?page=2",
            content_type="application/json",
            headers=self.headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.get_json()['listings']), 23)
        self.assertEqual(response.get_json()['pageNumber'], 2)
        self.assertEqual(response.get_json()['pageSize'], 23)
        self.assertEqual(response.get_json()['totalCount'], 73)
