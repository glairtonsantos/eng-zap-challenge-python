import os
import json
from unittest import TestCase
from flask_api import exceptions
from eng_zap_challenge_python.filters import BaseFilter

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(BASE_DIR, "source-sample.json")) as json_file:
    DATA_SOURCE = json.load(json_file)[0]


class MockFilter(BaseFilter):
    def expressions(self) -> bool:
        return True


class CustomBaseFilter(BaseFilter):
    def expressions(self) -> bool:
        return True


class NotImplementedExpressionFilter(BaseFilter):
    pass


class BaseFilterTest(TestCase):
    def setUp(self):
        self.content = DATA_SOURCE
        self.base_filter = MockFilter(self.content)

    def test_process_dict(self):
        source = "address__geoLocation__location__lon"
        value = self.base_filter.process_dict(source)

        self.assertEqual(float(value), -46.716542)

    def test_get_nested_dict(self):
        source = "address__geoLocation__location__lon"
        args = source.split("__")
        value = self.base_filter.get_nested_dict(self.content, args)

        self.assertEqual(float(value), -46.716542)

    def test_get_nested_dict_not_found_key(self):
        source = "address__geoLocation__location__lon__key"

        self.assertRaises(
            exceptions.APIException,
            self.base_filter.get_nested_dict,
            self.content,
            source.split("__"),
        )

    def test_get_nested_dict_key_error(self):
        source = "address__geoLocation__location__longitude"

        self.assertRaises(
            exceptions.APIException,
            self.base_filter.get_nested_dict,
            self.content,
            source.split("__"),
        )

    def test_get_nested_dict_without_key_value_default(self):
        source = "address__geoLocation__location__longitude"
        value_default = self.base_filter.get_nested_dict(
            self.content, source.split("__"), True, -23.588393
        )

        value_null = self.base_filter.get_nested_dict(
            self.content, source.split("__"), True
        )

        self.assertEqual(value_default, -23.588393)
        self.assertIsNone(value_null)

    def test_inside_bounding_box_true(self):
        custom_content = {
            "address": {
                "city": "",
                "neighborhood": "",
                "geoLocation": {
                    "precision": "ROOFTOP",
                    "location": {"lon": -46.66000, "lat": -23.55000},
                },
            }
        }

        custom_base_filter = CustomBaseFilter(custom_content)
        self.assertTrue(custom_base_filter.inside_bounding_box())

    def test_inside_bounding_box_false(self):
        custom_content = {
            "address": {
                "city": "",
                "neighborhood": "",
                "geoLocation": {
                    "precision": "ROOFTOP",
                    "location": {"lon": -46.70000, "lat": -23.55000},
                },
            }
        }

        custom_base_filter = CustomBaseFilter(custom_content)
        self.assertFalse(custom_base_filter.inside_bounding_box())

    def test_business_type(self):
        self.assertTrue(self.base_filter._get_business_type("SALE"))
        self.assertFalse(self.base_filter._get_business_type("RENTAL"))

    def test_is_rental(self):
        self.assertFalse(self.base_filter.is_rental())
        self.assertTrue(self.base_filter.is_sale())

    def test_is_sale(self):
        custom_content = {
            "pricingInfos": {
                "yearlyIptu": "0",
                "rentalTotalPrice": "500000",
                "businessType": "RENTAL",
                "monthlyCondoFee": "500",
            }
        }

        custom_base_filter = CustomBaseFilter(custom_content)

        self.assertTrue(custom_base_filter.is_rental())
        self.assertFalse(custom_base_filter.is_sale())

    def test_is_valid_location(self):
        custom_content = {
            "address": {
                "city": "",
                "neighborhood": "",
                "geoLocation": {
                    "precision": "ROOFTOP",
                    "location": {"lon": -46.716542, "lat": -23.502555},
                },
            }
        }

        custom_base_filter = CustomBaseFilter(custom_content)
        self.assertTrue(custom_base_filter._validate_location())

    def test_is_invalid_location(self):
        custom_content = {
            "address": {
                "city": "",
                "neighborhood": "",
                "geoLocation": {
                    "precision": "ROOFTOP",
                    "location": {"lon": 0, "lat": 0},
                },
            }
        }

        custom_base_filter = CustomBaseFilter(custom_content)
        self.assertFalse(custom_base_filter._validate_location())

    def test_is_eligible(self):
        self.assertTrue(self.base_filter.is_eligible())

    def test_is_not_eligible(self):
        custom_content = {
            "address": {
                "city": "",
                "neighborhood": "",
                "geoLocation": {
                    "precision": "ROOFTOP",
                    "location": {"lon": 0, "lat": 0},
                },
            }
        }

        custom_base_filter = CustomBaseFilter(custom_content)
        self.assertFalse(custom_base_filter.is_eligible())
