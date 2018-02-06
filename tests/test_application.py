from unittest import TestCase
from unittest.mock import MagicMock

import inject

from application.application_impl import ApplicationImpl
from fetcher import Fetcher


def test_config(binder):
    binder.bind_to_constructor(Fetcher, lambda: MagicMock())


class TestApplicationImpl(TestCase):
    def setUp(self):
        inject.clear_and_configure(test_config)
        self.app = ApplicationImpl()
        self.app.difference = 0.01

    def test_compare(self):
        data = [
            {'exchange_name': 'a', 'data': {'cur1/cur2': 1, 'cur1/cur3': 2}},  # should be in compare
            {'exchange_name': 'b', 'data': {'cur1/cur2': 1.1, 'cur1/cur3': 2.01}},  # not should
        ]

        res = self.app.compare(data)
        expected = {'cur1/cur2': {'a': 1, 'b': 1.1, 'diff': 0.1}}

        self.assertEqual(res, expected)
