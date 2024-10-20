from unittest                                           import TestCase
from starlette.testclient                                import TestClient
from cbr_shared.cbr_backend.session.DB_Session           import DB_Session
from cbr_shared.cbr_backend.session.DB_Sessions          import DB_Sessions
from cbr_shared.cbr_backend.users.DB_Users import DB_Users
from cbr_user_data.fast_api.routes.Routes__User          import Routes__User
from osbot_utils.utils.Dev                               import pprint
from tests.integration.cbr_shared__for_integration_tests import cbr_shared__assert_local_stack
from tests.integration.user_data__objs_for_tests         import fast_api__local_stack, fast_api__user_data__client


class test__client__Routes__User(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cbr_shared__assert_local_stack()
        cls.client          = fast_api__user_data__client
        cls.routes_user     = Routes__User()                        # to find this test via usage's mappings

    def test_setUpClass(self):
        assert type(self.client) is TestClient

    # todo: finish this test
    def test__user__profile(self):
        response = self.client.get("/user/user-profile")
        assert response.status_code == 200                  # BUG this should be 401
        assert response.json() == {"error":"User not authenticated"}
        # db_users = DB_Users()
        # pprint(db_users.db_users())
        # db_sessions = DB_Sessions()
        # pprint(db_sessions.s3_bucket())
        # pprint(db_sessions.s3().client().meta.endpoint_url)
        # pprint(list(db_sessions.sessions()))