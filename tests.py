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


if __name__ == '__main__':
    unittest.main(verbosity=2)
