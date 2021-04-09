from unittest import TestCase
from eng_zap_challenge_python.filters import ZapFilter


class ZapFilterTest(TestCase):
    def setUp(self):
        self.class_filter = ZapFilter

    def test_get_value_sale_minimal_inside_bounding_box(self):
        custom_content = {
            "pricingInfos": {
                "yearlyIptu": "0",
                "price": "700000",
                "businessType": "SALE",
                "monthlyCondoFee": "500",
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
        self.assertEqual(
            class_filter._get_value_sale_minimal(),
            class_filter.VALUE_MIN_SALE * (1 - class_filter.PER_BOUNDING_BOX),
        )

    def test_get_value_sale_minimal_outside_bounding_box(self):
        custom_content = {
            "pricingInfos": {
                "yearlyIptu": "0",
                "price": "700000",
                "businessType": "SALE",
                "monthlyCondoFee": "500",
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
            class_filter._get_value_sale_minimal(),
            class_filter.VALUE_MIN_SALE,
        )

    def test_if_eligible_rental(self):
        custom_content = {
            "pricingInfos": {
                "yearlyIptu": "0",
                "rentalTotalPrice": "3600",
                "businessType": "RENTAL",
                "monthlyCondoFee": "300",
            }
        }

        class_filter = self.class_filter(custom_content)
        self.assertTrue(class_filter._is_eligible_rental())

    def test_if_not_eligible_rental(self):
        custom_content = {
            "pricingInfos": {
                "yearlyIptu": "0",
                "rentalTotalPrice": "3400",
                "businessType": "RENTAL",
                "monthlyCondoFee": "300",
            }
        }

        class_filter = self.class_filter(custom_content)
        self.assertFalse(class_filter._is_eligible_rental())

    def test_if_value_sale_minimal(self):
        custom_content = {
            "pricingInfos": {
                "yearlyIptu": "0",
                "price": "650000",
                "businessType": "SALE",
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
        self.assertTrue(class_filter._is_price_sale_minimal())

    def test_if_value_sale_minimal_false(self):
        custom_content = {
            "pricingInfos": {
                "yearlyIptu": "0",
                "price": "590000",
                "businessType": "SALE",
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
        self.assertFalse(class_filter._is_price_sale_minimal())

    def test_value_usable_areas(self):
        custom_content = {"usableAreas": 150}

        class_filter = self.class_filter(custom_content)
        self.assertIsInstance(class_filter._get_value_usable_areas(), float)
        self.assertEqual(150.0, class_filter._get_value_usable_areas())

    def test_value_usable_areas_null(self):
        custom_content = {"usableAreas": ""}

        class_filter = self.class_filter(custom_content)
        self.assertEqual(0.0, class_filter._get_value_usable_areas())

    def test_if_value_usable_areas_minimal(self):
        custom_content = {"usableAreas": 3600}

        class_filter = self.class_filter(custom_content)
        self.assertTrue(class_filter._is_value_usable_areas_minimal())

    def test_if_not_value_usable_areas_minimal(self):
        custom_content = {"usableAreas": 3400}

        class_filter = self.class_filter(custom_content)
        self.assertFalse(class_filter._is_value_usable_areas_minimal())

    def test_if_value_usable_areas_minimal_is_valid(self):
        custom_content = {"usableAreas": 1}

        class_filter = self.class_filter(custom_content)
        self.assertTrue(class_filter._validate_usable_areas())

    def test_if_value_usable_areas_minimal_is_invalid(self):
        custom_content = {"usableAreas": 0}

        class_filter = self.class_filter(custom_content)
        self.assertFalse(class_filter._validate_usable_areas())

    def test_is_eligible_sale(self):
        custom_content = {
            "usableAreas": 3600,
            "pricingInfos": {
                "yearlyIptu": "0",
                "price": "700000",
                "businessType": "SALE",
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
        self.assertTrue(class_filter._validate_usable_areas())
        self.assertTrue(class_filter._is_price_sale_minimal())
        self.assertTrue(class_filter._is_value_usable_areas_minimal())
        self.assertTrue(class_filter._is_eligible_sale())

    def test_is_expressions_is_valid(self):
        custom_content = {
            "usableAreas": 3600,
            "pricingInfos": {
                "yearlyIptu": "0",
                "price": "700000",
                "businessType": "SALE",
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
        self.assertFalse(class_filter._is_eligible_rental())
        self.assertTrue(class_filter._is_eligible_sale())
        self.assertTrue(class_filter.expressions())
