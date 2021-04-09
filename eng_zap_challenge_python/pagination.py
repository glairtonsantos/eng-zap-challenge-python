from flask_api import exceptions


class SourcePagination:
    PAGE_NUMBER = 1
    PAGE_SIZE = 50

    def __init__(self, args={}, data=[]):
        self.args = args
        self.data = data

    def _page_number(self) -> int:
        return int(self.args.get("page", self.PAGE_NUMBER))

    def _get_page_size(self) -> int:
        return int(self.args.get("page_size", self.PAGE_SIZE))

    def _split_pages(self) -> list:
        """
        return list with list's contain page_size elements
        """
        try:
            return [
                self.data[i: i + self._get_page_size()]
                for i in range(0, len(self.data), self._get_page_size())
            ]
        except ValueError:
            raise exceptions.ParseError("query param `page_size` is invalid")

    def _get_paginated_data(self) -> list:
        splited_pages = self._split_pages()

        if len(splited_pages) >= self._page_number():
            return splited_pages[self._page_number() - 1] if self.data else []
        else:
            raise exceptions.NotFound

    def response(self) -> dict:
        paginated = self._get_paginated_data()
        return {
            "pageNumber": self._page_number(),
            "pageSize": len(paginated),
            "totalCount": len(self.data),
            "listings": paginated,
        }
