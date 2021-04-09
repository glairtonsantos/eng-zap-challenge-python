from unittest import TestCase
from eng_zap_challenge_python.filters import VivaRealFilter


class VivaRealFilterTest(TestCase):
    def setUp(self):
        self.class_filter = VivaRealFilter

    def test_get_value_rental_maximum_inside_dounding_box(self):
        custom_content = {
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

        class_filter = self.class_filter(custom_content)
        perc = 1 + class_filter.PER_BOUNDING_BOX
        self.assertEqual(
            class_filter._get_value_rental_maximum(),
            class_filter.VALUE_MAX_RENTAL * perc,
        )

    def test_get_value_rental_maximum_outside_bounding_box(self):
        custom_content = {
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
                    "location": {"lon": -46.650000, "lat": -23.530000},
                },
            },
        }

        class_filter = self.class_filter(custom_content)
        self.assertEqual(
            class_filter._get_value_rental_maximum(),
            class_filter.VALUE_MAX_RENTAL
        )

    def test_is_eligible_rental(self):
        custom_content = {
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

        class_filter = self.class_filter(custom_content)
        self.assertTrue(class_filter.is_rental())
        self.assertTrue(class_filter._is_price_rental_maximum())
        self.assertTrue(class_filter._is_valid_monthly_condo_fee())
        self.assertTrue(class_filter._is_value_monthly_condo_fee_maximum())
        self.assertTrue(class_filter._is_eligible_rental())

    def test_is_eligible_sale(self):
        custom_content = {
            "pricingInfos": {
                "yearlyIptu": "0",
                "price": "690000",
                "businessType": "SALE",
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

        class_filter = self.class_filter(custom_content)
        self.assertTrue(class_filter.is_sale())
        self.assertTrue(class_filter._is_price_sale_maximum())
        self.assertTrue(class_filter._is_eligible_sale())

    def test_is_valid_monthly_condo_fee(self):
        custom_content = {
            "pricingInfos": {
                "yearlyIptu": "0",
                "rentalTotalPrice": "3600",
                "businessType": "RENTAL",
                "monthlyCondoFee": "200",
            }
        }
        class_filter = self.class_filter(custom_content)
        self.assertTrue(class_filter._is_valid_monthly_condo_fee())

    def test_is_invalid_monthly_condo_fee_null(self):
        custom_content = {
            "pricingInfos": {
                "yearlyIptu": "0",
                "rentalTotalPrice": "3600",
                "businessType": "RENTAL",
            }
        }
        class_filter = self.class_filter(custom_content)
        self.assertFalse(class_filter._is_valid_monthly_condo_fee())

    def test_is_invalid_numeric_monthly_condo_fee(self):
        custom_content = {
            "pricingInfos": {
                "yearlyIptu": "0",
                "rentalTotalPrice": "3600",
                "businessType": "RENTAL",
                "monthlyCondoFee": "-0,01",
            }
        }
        class_filter = self.class_filter(custom_content)
        self.assertFalse(class_filter._is_valid_monthly_condo_fee())

    def test_is_invalid_string_monthly_condo_fee(self):
        custom_content = {
            "pricingInfos": {
                "yearlyIptu": "0",
                "rentalTotalPrice": "3600",
                "businessType": "RENTAL",
                "monthlyCondoFee": "AAA",
            }
        }
        class_filter = self.class_filter(custom_content)
        self.assertFalse(class_filter._is_valid_monthly_condo_fee())

    def test_is_expressions_is_valid(self):
        custom_content = {
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

        class_filter = self.class_filter(custom_content)
        self.assertFalse(class_filter._is_eligible_sale())
        self.assertTrue(class_filter._is_eligible_rental())
        self.assertTrue(class_filter.expressions())
