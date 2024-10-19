from unittest                                                     import TestCase

from starlette.testclient import TestClient

from cbr_user_data.fast_api.routes.Routes__Info       import Routes__Info
from cbr_user_data.utils.Version import version__cbr_user_data
from tests.integration.user_data__objs_for_tests import fast_api__local_stack, fast_api__user_data__client


class test__client__Routes__User_Data(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.client          = fast_api__user_data__client

    def test_setUpClass(self):
        assert type(self.client) is TestClient

    def test__info__ping(self):
        response = self.client.get("/info/ping")
        assert response.status_code == 200
        assert response.json()      == {"pong": '42'}

    def test__info__version(self):
        response = self.client.get("/info/version")
        assert response.status_code == 200
        assert response.json()      == {"version": version__cbr_user_data}