from unittest                                   import TestCase
from cbr_user_data.fast_api.routes.Routes__Info import Routes__Info
from cbr_user_data.utils.Version import version__cbr_user_data


class test_Routes_Info(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.routes_info = Routes__Info()

    def test_ping(self):
        assert self.routes_info.ping() == {"pong": '42'}

    def test_version(self):
        assert self.routes_info.version() == {"version": version__cbr_user_data }

    def test_setup_routes(self):
        assert self.routes_info.routes_paths() == []
        assert self.routes_info.setup_routes() == self.routes_info
        assert self.routes_info.routes_paths() == ['/ping', '/version']
