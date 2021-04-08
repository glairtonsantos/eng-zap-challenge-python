from abc import ABC, abstractmethod
from flask_api import exceptions


class BaseFilter(ABC):

    # Bounding Box Grupo ZAP
    MIN_LON = -46.693419
    MIN_LAT = -23.568704
    MAX_LON = -46.641146
    MAX_LAT = -23.546686

    def __init__(self, content):
        self.content = content

    @abstractmethod
    def expressions(self) -> bool:
        pass

    def get_nested_dict(self, content, args):
        """
        return value in nested content by args splited:
        source = "keyA__keyB__keyC"
            {
                "keyA": {
                    "keyB": {
                        "keyC": value
                    }
                }
            }
        """
        try:
            return (
                content[args[0]]
                if len(args) == 1
                else self.get_nested_dict(content[args[0]], args[1:])
            )
        except KeyError:
            pass

    def process_dict(self, source):
        return self.get_nested_dict(self.content, source.split("__"))

    def inside_bounding_box(self) -> bool:
        location = "address__geoLocation__location"
        lon = self.process_dict(f"{location}__lon")
        lat = self.process_dict(f"{location}__lat")

        lon_inside = float(lon) >= self.MIN_LON and float(lon) <= self.MAX_LON
        lat_inside = float(lat) >= self.MIN_LAT and float(lat) <= self.MAX_LAT

        return lon_inside and lat_inside

    def _get_business_type(self, business):
        value = self.process_dict("pricingInfos__businessType")
        return value == business

    def is_rental(self) -> bool:
        return self._get_business_type("RENTAL")

    def is_sale(self) -> bool:
        return self._get_business_type("SALE")

    def _validate_location(self) -> bool:
        location = "address__geoLocation__location"
        lon = self.process_dict(f"{location}__lon")
        lat = self.process_dict(f"{location}__lat")

        return float(lon) != 0 or float(lat) != 0

    def is_eligible(self) -> bool:
        return self._validate_location() and self.expressions()


class ZapFilter(BaseFilter):
    VALUE_MIN_SALE = 600000
    VALUE_MIN_RENTAL = 3500
    VALUE_MIN_USABLE_AREAS = 3500
    PER_BOUNDING_BOX = 0.1

    def expressions(self) -> bool:
        is_eligible_rental = self._is_eligible_rental()
        is_eligible_sale = self._is_eligible_sale()
        return is_eligible_rental or is_eligible_sale

    def _get_value_sale_minimal(self) -> float:
        return (
            self.VALUE_MIN_SALE - self.VALUE_MIN_SALE * self.PER_BOUNDING_BOX
            if self.inside_bounding_box()
            else self.VALUE_MIN_SALE
        )

    def _is_eligible_rental(
        self,
    ) -> bool:
        is_rental = self.is_rental()
        return is_rental and self._is_price_rental_minimal()

    def _is_price_rental_minimal(
        self,
    ) -> bool:
        value = self.process_dict("pricingInfos__rentalTotalPrice")
        return float(value) >= self.VALUE_MIN_RENTAL

    def _is_price_sale_minimal(self) -> bool:
        value = self.process_dict("pricingInfos__price")
        return float(value) >= self._get_value_sale_minimal()

    def _get_value_usable_areas(self) -> float:
        value = self.process_dict("usableAreas")
        return float(value)

    def _is_value_usable_areas_minimal(self) -> bool:
        value = self._get_value_usable_areas()
        return value > self.VALUE_MIN_USABLE_AREAS

    def _validate_usable_areas(self) -> bool:
        value = self._get_value_usable_areas()
        return value > 0

    def _is_eligible_sale(self) -> bool:
        return (
            self.is_sale()
            and self._validate_usable_areas()
            and self._is_price_sale_minimal()
            and self._is_value_usable_areas_minimal()
        )


class VivaRealFilter(BaseFilter):
    VALUE_MAX_RENTAL = 4000
    VALUE_MAX_SALE = 700000
    PER_BOUNDING_BOX = 0.5
    PER_VALUE_RENTAL = 0.3

    def expressions(self) -> bool:
        eligible_rental = self._is_eligible_rental()
        eligible_sale = self._is_eligible_sale()
        return eligible_rental or eligible_sale

    def _get_value_rental_maximum(self) -> float:
        value_percent = self.VALUE_MAX_RENTAL * self.PER_BOUNDING_BOX
        return (
            self.VALUE_MAX_RENTAL + value_percent
            if self.inside_bounding_box()
            else self.VALUE_MAX_RENTAL
        )

    def _is_eligible_rental(self) -> bool:
        return (
            self.is_rental()
            and self._is_price_rental_maximum()
            and self._is_valid_monthly_condo_fee()
            and self._is_value_monthly_condo_fee_maximum()
        )

    def _is_eligible_sale(self) -> bool:
        return self.is_sale() and self._is_price_sale_maximum()

    def _get_value_rental(self) -> float:
        value = self.process_dict("pricingInfos__rentalTotalPrice")
        return float(value)

    def _is_price_rental_maximum(self) -> bool:
        value_rental_maximum = self._get_value_rental_maximum()
        value_rental = self._get_value_rental()
        return value_rental <= value_rental_maximum

    def _is_price_sale_maximum(self) -> bool:
        value = self.process_dict("pricingInfos__price")
        return float(value) <= self.VALUE_MAX_SALE

    def _is_valid_monthly_condo_fee(self) -> bool:
        value = self.process_dict("pricingInfos__monthlyCondoFee")
        return value is not None and value.isnumeric()

    def _is_value_monthly_condo_fee_maximum(self) -> bool:
        source = "pricingInfos__monthlyCondoFee"
        monthly_condo_fee_value = self.process_dict(source)
        limit_condo_fee = self._get_value_rental() * self.PER_VALUE_RENTAL
        return float(monthly_condo_fee_value) < limit_condo_fee


class SourceFilter:
    CLASS_FILTER = {"zap": ZapFilter, "viva-real": VivaRealFilter}

    def __init__(self, context, data_source=[]):
        self.context = context
        self.data_source = data_source
        self.class_filter = self._get_class_filter()

    def _get_class_filter(self) -> BaseFilter:
        try:
            return self.CLASS_FILTER[self.context]
        except KeyError:
            raise exceptions.NotFound()

    def _rules_class(self, content) -> bool:
        class_filter = self.class_filter(content)
        return class_filter.is_eligible()

    def filter(self) -> list:
        filtered = list(
            filter(
                self._rules_class,
                self.data_source,
            )
        )

        return filtered
