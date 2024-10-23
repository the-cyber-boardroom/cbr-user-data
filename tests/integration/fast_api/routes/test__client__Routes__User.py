from unittest                                       import TestCase
from starlette.testclient                           import (TestClient)
from cbr_user_data.fast_api.routes.Routes__User     import Routes__User
from tests.integration.user_data__objs_for_tests    import fast_api__user_data__client, user_data__assert_local_stack


class test__client__Routes__User(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        user_data__assert_local_stack()
        cls.client          = fast_api__user_data__client
        cls.routes_user     = Routes__User()                        # to find this test via usage's mappings

    def test_setUpClass(self):
        assert type(self.client) is TestClient

    # todo: finish this test
    def test__user__profile(self):
        response = self.client.get("/user/user-profile")
        assert response.status_code == 200                  # BUG this should be 401
        assert response.json() == {'data'   : None  ,
                                   'error'  : None  ,
                                   'message': 'Session not found from the current request data',
                                   'status' : 'error'}
        # db_users = DB_Users()
        # pprint(db_users.db_users())
        # db_sessions = DB_Sessions()
        # pprint(db_sessions.s3_bucket())
        # pprint(db_sessions.s3().client().meta.endpoint_url)
        # pprint(list(db_sessions.sessions()))