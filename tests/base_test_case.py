import unittest
import json

from app import create_app, db
from config import Config
from app.models import LogisticMeshMap


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.test_rctx = self.app.test_request_context()
        self.adapter = self.app.url_map.bind('')
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def _create_map_sp(self):
        data_map = """A B 10
        B D 15
        A C 20
        C D 30
        B E 50
        D E 30"""

        lm_map = LogisticMeshMap()
        lm_map.mapname = 'mapa sp'
        log_map = [s.rstrip().split() for s in data_map.split('\n')]
        lm_map.routes = json.dumps(log_map)
        db.session.add(lm_map)
        db.session.commit()

    def _create_map_sc(self):
        data_map = """A C 20
        C E 30
        B C 15
        A B 10
        B D 50
        D E 30"""

        lm_map = LogisticMeshMap()
        lm_map.mapname = 'mapa sc'
        log_map = [s.rstrip().split() for s in data_map.split('\n')]
        lm_map.routes = json.dumps(log_map)
        db.session.add(lm_map)
        db.session.commit()
