from unittest import TestCase
from flask_api.exceptions import NotFound
from eng_zap_challenge_python.filters import SourceFilter, ZapFilter


class SourceFilterTest(TestCase):
    def setUp(self):
        self.class_filter = SourceFilter

    def test_instance_class(self):
        source_filter_class = self.class_filter("zap")

        self.assertTrue(
            type(source_filter_class.class_filter) == type(ZapFilter)
        )
        self.assertEqual(source_filter_class.context, "zap")
        self.assertEqual(source_filter_class.data_source, [])

    def test_get_class_filter_invalid(self):
        self.assertRaises(NotFound, self.class_filter, "5andar")

    def test_rules_class(self):
        custom_data_source = [
            {
                "pricingInfos": {
                    "yearlyIptu": "0",
                    "rentalTotalPrice": "3900",
                    "businessType": "RENTAL",
                    "monthlyCondoFee": "200",
                },
                "address": {
                    "city": "",
                    "neighborhood": "",
                    "geoLocation": {
                        "precision": "ROOFTOP",
                        "location": {"lon": -46.650000, "lat": -23.550000},
                    },
                },
            }
        ]

        source_filter_class = self.class_filter(
            "viva-real",
            custom_data_source
        )

        self.assertTrue(
            source_filter_class._rules_class(custom_data_source[0])
        )

    def test_filter_data_source(self):
        custom_data_source = [
            {
                "pricingInfos": {
                    "yearlyIptu": "0",
                    "rentalTotalPrice": "3900",
                    "businessType": "RENTAL",
                    "monthlyCondoFee": "200",
                },
                "address": {
                    "city": "",
                    "neighborhood": "",
                    "geoLocation": {
                        "precision": "ROOFTOP",
                        "location": {"lon": -46.650000, "lat": -23.550000},
                    },
                },
            },
            {
                "pricingInfos": {
                    "yearlyIptu": "0",
                    "price": "900000",
                    "businessType": "SALE",
                    "monthlyCondoFee": "1500",
                },
                "address": {
                    "city": "",
                    "neighborhood": "",
                    "geoLocation": {
                        "precision": "ROOFTOP",
                        "location": {"lon": -46.650000, "lat": -23.550000},
                    },
                },
            },
        ]

        source_filter_class = self.class_filter(
            "viva-real",
            custom_data_source
        )
        filtered = source_filter_class.filter()

        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0], custom_data_source[0])
