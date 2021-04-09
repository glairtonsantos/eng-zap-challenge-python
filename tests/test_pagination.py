from unittest import TestCase
from flask_api.exceptions import ParseError, NotFound
from eng_zap_challenge_python.pagination import SourcePagination


class SourcePaginationTest(TestCase):
    def setUp(self):
        self.class_paginate = SourcePagination

    def test_instance_class(self):
        class_paginate = self.class_paginate()

        self.assertEqual(class_paginate.args, {})
        self.assertEqual(class_paginate.data, [])

    def test_page_numb_default(self):
        class_paginate = self.class_paginate()

        self.assertEqual(
            class_paginate._page_number(),
            class_paginate.PAGE_NUMBER
        )

    def test_page_size_default(self):
        class_paginate = self.class_paginate()

        self.assertEqual(
            class_paginate._get_page_size(),
            class_paginate.PAGE_SIZE
        )

    def test_page_number_defined(self):
        class_paginate = self.class_paginate({"page": 1})

        self.assertEqual(class_paginate._page_number(), 1)

    def test_page_size_defined(self):
        class_paginate = self.class_paginate({"page_size": 10})

        self.assertEqual(class_paginate._get_page_size(), 10)

    def test_split_pages(self):
        data = range(10)

        class_paginate = self.class_paginate({"page_size": 2}, data)
        pages = class_paginate._split_pages()

        """
        5 pages with 2 registers
        """
        self.assertEqual(len(pages), 5)

    def test_page_size_invalid(self):
        data = range(10)

        class_paginate = self.class_paginate({"page_size": 0}, data)
        self.assertRaises(ParseError, class_paginate._split_pages)

        class_paginate = self.class_paginate({"page_size": "AAA"}, data)
        self.assertRaises(ParseError, class_paginate._split_pages)

    def test_paginated_data(self):
        data = range(9)

        """
        5 pages = 4 pages with 2 registers; 1 page with 1 register
        """
        class_paginate = self.class_paginate({"page_size": 2}, data)
        paginated = class_paginate._get_paginated_data()

        # default page = 1
        self.assertEqual(len(paginated), 2)

        class_paginate = self.class_paginate({"page_size": 2, "page": 5}, data)
        paginated = class_paginate._get_paginated_data()

        # last page have 1 register
        self.assertEqual(len(paginated), 1)

        class_paginate = self.class_paginate({"page_size": 2}, [])

        self.assertRaises(NotFound, class_paginate._get_paginated_data)

    def test_response_paginated(self):
        data = range(9)

        """
        5 pages = 4 pages with 2 registers; 1 page with 1 register
        """
        class_paginate = self.class_paginate({"page_size": 2, "page": 3}, data)
        response = class_paginate.response()

        self.assertEqual(
            response,
            {
                "pageNumber": 3,
                "pageSize": 2,
                "totalCount": 9,
                "listings": range(4, 6)
            },
        )
