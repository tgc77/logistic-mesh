#!/usr/bin/env python
import unittest
from werkzeug.exceptions import NotFound
from app import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.adapter = app.url_map.bind('')

    def tearDown(self):
        self.app_context.pop()

    def test_index_page_should_exists(self):
        res = self.client.get('/index')
        self.assertEqual(res.status_code, 200)

    def test_wrong_index_page_should_raises_not_found_exception(self):
        with self.assertRaises(NotFound) as context:
            self.adapter.match('/wrong_index')

# A D
    # parent = {'A': None, 'B': 'A', 'C': 'A', 'D': 'B', 'E': 'B'}
    # dist = {'A': 0, 'B': 10, 'C': 20, 'D': 25, 'E': 60}

    # A E
    # parent = {'A': None, 'B': 'A', 'C': 'A', 'D': 'B', 'E': 'D'}
    # dist = {'A': 0, 'B': 10, 'C': 20, 'D': 25, 'E': 55}

    # result = {}
    # result['mapname'] = 'mapa sp'
    # result['best_route'] = print_path(target='E', parent=parent)
    # result['cost'] = 6.5


if __name__ == '__main__':
    unittest.main(verbosity=2)
