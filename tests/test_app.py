from werkzeug.exceptions import NotFound
from html.parser import HTMLParser

from tests.base_test_case import BaseTestCase


class MyHTMLParser(HTMLParser):
    def __init__(self) -> None:
        HTMLParser.__init__(self)
        self._lookup_tag = None
        self._is_lookup_tag = False

    def lookup_tag(self, tag):
        self._lookup_tag = tag

    def read(self, data):
        # clear the current output before re-use
        self._lines = []
        # re-set the parser's state before re-use
        self.reset()
        self.feed(data)
        return self._lines

    def handle_starttag(self, tag, attrs):
        if tag == self._lookup_tag:
            self._is_lookup_tag = True

    def handle_endtag(self, tag):
        if tag == self._lookup_tag:
            self._is_lookup_tag = False

    def handle_data(self, data):
        if self._is_lookup_tag:
            self._lines.append(data)


class TestAppCase(BaseTestCase):

    def test_index_page_should_exists(self):
        res = self.client.get('/index', follow_redirects=True)
        self.assertEqual(res.status_code, 200)

    def test_wrong_index_page_should_raises_not_found_exception(self):
        with self.assertRaises(NotFound) as _:
            self.adapter.match('/wrong_index')

    def test_upload_map(self):
        res = self.client.get('/upload_map', follow_redirects=True)
        self.assertEqual(res.status_code, 200)

        data = dict(
            mapname='mapa sp',
            routes="A B 10\nB C 20\nC D 15"
        )
        res = self.client.post('/upload_map', data=data, follow_redirects=True,
                               headers={"Content-Type": "application/x-www-form-urlencoded"})
        self.assertEqual(res.status_code, 200)

    def test_upload_map_should_abort_with_400_status_code(self):
        data = dict(
            mapname='mapa sp',
            routes="4 B 10\nB C 20\nC D 15"
        )
        res = self.client.post('/upload_map', data=data, follow_redirects=True,
                               headers={"Content-Type": "application/x-www-form-urlencoded"})
        self.assertEqual(res.status_code, 400)

    def test_list_maps(self):
        """Testing with any map saved into database"""
        res = self.client.get('/list_maps', follow_redirects=True)
        self.assertEqual(res.status_code, 200)

        self._create_map_sc()

        """Testing with one map saved into database"""
        res = self.client.get('/list_maps', follow_redirects=True)
        self.assertEqual(res.status_code, 200)

    def test_find_best_route(self):
        res = self.client.get('/find_best_route', follow_redirects=True)
        self.assertEqual(res.status_code, 200)

        self._create_map_sp()

        form_data = dict(
            mapname='mapa sp', origin='A', destiny='D',
            truck_autonomy=10, liter_fuel_value=2.5
        )
        res = self.client.post('/find_best_route', data=form_data, follow_redirects=True,
                               headers={"Content-Type": "application/x-www-form-urlencoded"})
        self.assertEqual(res.status_code, 200)

        """Get response data from best route template html"""
        html_data = res.get_data(True)
        parser = MyHTMLParser()
        parser.lookup_tag('span')
        best_route_data = parser.read(html_data)
        expected = ['mapa sp', "['A', 'B', 'D']", '6.25']
        self.assertListEqual(best_route_data, expected)

    def test_best_route_do_not_exist(self):
        self._create_map_sp()

        form_data = dict(
            mapname='mapa sp', origin='E', destiny='A',
            truck_autonomy=10, liter_fuel_value=2.5
        )
        res = self.client.post('/find_best_route', data=form_data, follow_redirects=True,
                               headers={"Content-Type": "application/x-www-form-urlencoded"})
        self.assertEqual(res.status_code, 200)

        """Get response data from best route template html"""
        html_data = res.get_data(True)
        parser = MyHTMLParser()
        parser.lookup_tag('span')
        best_route_data = parser.read(html_data)
        expected = ['mapa sp', '[]', '0.0']
        self.assertListEqual(best_route_data, expected)

    def test_find_best_route_with_wrong_origin_should_abort_bad_request(self):
        self._create_map_sp()

        form_data = dict(
            mapname='mapa sp', origin=9, destiny='D',
            truck_autonomy=10, liter_fuel_value=2.5
        )
        res = self.client.post('/find_best_route', data=form_data, follow_redirects=True,
                               headers={"Content-Type": "application/x-www-form-urlencoded"})
        self.assertEqual(res.status_code, 400)

        """Get response data from error into template html"""
        html_data = res.get_data(True)
        parser = MyHTMLParser()
        parser.lookup_tag('h1')
        lookup_data = parser.read(html_data)
        expected = "400 Bad Request: Field 'origin' must be a letter in the range: [A, B, C, D, E]"
        self.assertEqual(lookup_data[0], expected)
