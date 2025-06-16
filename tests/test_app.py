import unittest

from injector import Injector

from app import AppModule


class TestDependencyInjection(unittest.TestCase):
    def setUp(self):
        self.injector = Injector(AppModule)

    def test_home_page(self):
        from app import create_app
        app = create_app()
        with app.test_client() as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 200)
