from flask_api import exceptions


def try_convert_int(access):
    def wrapper(*args, **kwargs):
        try:
            return access(*args, **kwargs)
        except ValueError:
            raise exceptions.ParseError("query param is invalid value")

    return wrapper


class SourcePagination:
    PAGE_NUMBER = 1
    PAGE_SIZE = 50

    def __init__(self, args={}, data=[]):
        self.args = args
        self.data = data

    @try_convert_int
    def _page_number(self) -> int:
        return int(self.args.get("page", self.PAGE_NUMBER))

    @try_convert_int
    def _get_page_size(self) -> int:
        return int(self.args.get("page_size", self.PAGE_SIZE))

    def _split_pages(self) -> list:
        """
        return list with list's contain page_size elements
        """
        try:
            return [
                self.data[i : i + self._get_page_size()]
                for i in range(0, len(self.data), self._get_page_size())
            ]
        except ValueError:
            raise exceptions.ParseError("query param `page_size` is invalid")

    def _get_paginated_data(self) -> list:
        splited_pages = self._split_pages()
        is_positive = self._page_number() > 0
        try:
            if is_positive and len(splited_pages) >= self._page_number():
                return (
                    splited_pages[self._page_number() - 1]
                    if self.data
                    else []
                )
            else:
                raise exceptions.NotFound
        except IndexError:
            raise exceptions.ParseError(
                f"page size `{self._get_page_size()}` is invalid value"
            )

    def response(self) -> dict:
        paginated = self._get_paginated_data()
        return {
            "pageNumber": self._page_number(),
            "pageSize": len(paginated),
            "totalCount": len(self.data),
            "listings": paginated,
        }
